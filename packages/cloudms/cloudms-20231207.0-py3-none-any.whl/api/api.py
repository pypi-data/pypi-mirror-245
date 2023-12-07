import logging
import asyncio
import json
import hmac
import hashlib
import time
import websockets
from fastapi import WebSocket
from fastapi.responses import FileResponse

from common import util, config
from openstack.keystone import Auth

log = logging.getLogger("uvicorn")


def get_health():
    return util.response(200, data="OK")


def get_config():
    conf_default = config.config["DEFAULT"]
    conf = {
        "project_name": "Cloud User Portal",
        "support_email": "support@support",
        "doc_url": "http://doc",
        "obj_store_share_url": "http://obj-store"
    }
    for key in conf.keys():
        conf_key = key.replace("_", "-")
        if conf_key in conf_default:
            conf[key] = conf_default[conf_key]

    zones = []
    for zone in config.config.sections():
        if zone == "DEFAULT":
            continue
        zones.append({
            "description": config.config[zone]["description"],
            "portal_url": config.config[zone]["portal-url"],
            "name": zone
        })

    conf["available_zones"] = zones

    return util.response(200, data=conf)


def get_assets(file_name):
    mtype_map = {
        "js": "application/javascript",
        "css": "text/css",
        "ico": "image/svg+xml",
        "svg": "image/svg+xml",
        "png": "image/x-png"
    }
    ext = file_name.split(".")[-1]
    try:
        mtype = mtype_map[ext]
    except KeyError:
        log.error(f"Invalid extension {ext}!")
        return util.response(404)
    return FileResponse(f"static/assets/{file_name}", media_type=mtype)


def get_portal(path):
    hops = path.split("/")
    if hops[1] == "assets":
        return get_assets(hops[2])
    else:
        return FileResponse("static/index.html", media_type="text/html")


async def get_obj_url(req):
    req_data = await req.json()
    method = "GET"
    token_pack = await validate_token(req)
    catalog = token_pack["catalog"]
    svc_url = util.get_svc_url(catalog, "object-store")
    if "expire" not in req_data:
        req_data["expire"] = 3600
    try:
        a = svc_url.split("swift")
        host = f"{a[0]}swift"
        path = f"{a[1]}/{req_data['container']}/{req_data['object']}"
        key = req_data["key"]
        expire = int(time.time() + req_data["expire"])
    except KeyError:
        log.error(f"Invalid request {req_data}!")
        return util.response(400)
    body = f"{method}\n{expire}\n{path}"
    sig = hmac.new(key.encode(), body.encode(), hashlib.sha1).hexdigest()
    url = f"{host}{path}?temp_url_sig={sig}&temp_url_expires={expire}"
    return util.response(200, data={"url": url})


async def validate_token(req):
    token_pack = await Auth(config.svc_token_pack).validate(
            req.headers["x-auth-token"])
    if not token_pack:
        log.info("Auth token validation failed!")
        return
    token_pack["token"] = req.headers["x-auth-token"]
    return token_pack


async def api_auth_token(req):
    url = config.zone_conf["auth-url"] + "/auth/tokens"
    req_headers = {"Content-Type": "application/json"}
    data = await req.body()
    resp = await util.send_req("post", url, req_headers, data)
    resp_headers = {"x-subject-token": resp["headers"].get("x-subject-token")}
    return util.response(resp["status"], headers=resp_headers,
            data=resp["data"])


async def op_api(req, op, fwd_svc, fwd_path):
    if "x-auth-token" not in req.headers:
        return util.response(401, data={"message": "Auth token is missing!"})
    token_pack = await validate_token(req)
    if not token_pack:
        return util.response(401, data={"message": "Token validation failed!"})
    if "catalog" in token_pack:
        catalog = token_pack["catalog"]
    else:
        catalog = config.svc_token_pack["catalog"]
    svc_url = util.get_svc_url(catalog, fwd_svc)
    if fwd_svc in svc_hdlr_map:
        hdlr = svc_hdlr_map[fwd_svc]
        return await hdlr(req, op, svc_url, fwd_path, catalog)
    if req.query_params:
        fwd_path = f"{fwd_path}?{req.query_params}"
    data = await req.body()
    resp = await util.send_req(op, svc_url + fwd_path, req.headers, data)
    return util.response(resp["status"], data=resp["data"])


async def svc_hdlr_network(req, op, svc_url, fwd_path, catalog):
    hops = req.url.path.split("/")
    fwd_body = await req.body()
    fwd_headers = req.headers
    if hops[3] == "router":
        if op == "put":
            req_dict = json.loads(fwd_body.decode("utf-8"))
            if hops[-1] == "action":
                action = list(req_dict.keys())[0]
                fwd_path = f"{fwd_path}/{action}"
                fwd_body = json.dumps(req_dict[action]).encode("utf-8")
                # Reset headers to remove content-length because data length
                # is changed.
                fwd_headers = {"Content-Type": "application/json",
                        "x-auth-token": req.headers.get("x-auth-token")}
    if req.query_params:
        fwd_path = f"{fwd_path}?{req.query_params}"
    resp = await util.send_req(op, svc_url + fwd_path, fwd_headers, fwd_body)
    return util.response(resp["status"], data=resp["data"])


async def svc_hdlr_block(req, op, svc_url, fwd_path, catalog):
    hops = req.url.path.split("/")
    fwd_body = await req.body()
    fwd_headers = req.headers
    if hops[3] == "volume":
        if op == "post":
            req_dict = json.loads(fwd_body.decode("utf-8"))
            if hops[-1] == "action":
                action = list(req_dict.keys())[0]
                if action == "rollback":
                    svc_url = util.get_svc_url(catalog, "cms-backup")
                    fwd_path = fwd_path.replace("volumes", "volume")
            elif hops[-1] == "volume":
                if "backup_id" in req_dict["volume"]:
                    svc_url = util.get_svc_url(catalog, "cms-backup")
                    fwd_path = fwd_path.replace("volumes", "volume")
    if req.query_params:
        fwd_path = f"{fwd_path}?{req.query_params}"
    resp = await util.send_req(op, svc_url + fwd_path, fwd_headers, fwd_body)
    return util.response(resp["status"], data=resp["data"])


async def svc_hdlr_compute(req, op, svc_url, fwd_path, catalog):
    hops = req.url.path.split("/")
    fwd_body = await req.body()
    fwd_headers = req.headers
    if hops[3] == "instance":
        if op == "post":
            req_dict = json.loads(fwd_body.decode("utf-8"))
            if hops[-1] == "action":
                action = list(req_dict.keys())[0]
                if action == "rollback":
                    svc_url = util.get_svc_url(catalog, "cms-backup")
                    fwd_path = fwd_path.replace("servers", "instance")
    if req.query_params:
        fwd_path = f"{fwd_path}?{req.query_params}"
    resp = await util.send_req(op, svc_url + fwd_path, fwd_headers, fwd_body)
    return util.response(resp["status"], data=resp["data"])


async def svc_hdlr_obj_store(req, op, svc_url, fwd_path, catalog):
    hops = req.url.path.split("/")
    fwd_body = await req.body()
    fwd_headers = req.headers
    type_json = True
    if op == "get":
        if len(hops) == 5:
            type_json = False
    if req.query_params:
        fwd_path = f"{fwd_path}?{req.query_params}"
    resp = await util.send_req(op, svc_url + fwd_path, fwd_headers, fwd_body,
        type_json=type_json)
    return util.response(resp["status"], data=resp["data"])


async def _bridge_forward(ws_from: WebSocket,
        ws_to: websockets.WebSocketClientProtocol):
    while True:
        data = await ws_from.receive_text()
        await ws_to.send(data)


async def _bridge_reverse(ws_from: WebSocket,
        ws_to: websockets.WebSocketClientProtocol):
    while True:
        data = await ws_to.recv()
        await ws_from.send_text(data)


async def websocket_bridge(ws_a: WebSocket, ws_b_uri: str):
    zone = config.config["DEFAULT"]["zone"]
    api_url = config.config[f"zone.{zone}"]["cms-host"]
    config.load("cloudshell")
    port = config.config["DEFAULT"]["server-port"]
    config.load("api")
    
    await ws_a.accept()
    async with websockets.connect(f"wss://{api_url}: \
            {port}/v1{ws_b_uri}") as ws_b_client:
        loop = asyncio.get_event_loop()
        fwd_task = loop.create_task(_bridge_forward(ws_a, ws_b_client))
        rev_task = loop.create_task(_bridge_reverse(ws_a, ws_b_client))
        await asyncio.gather(fwd_task, rev_task)


svc_hdlr_map = {"network": svc_hdlr_network,
        "volumev3": svc_hdlr_block,
        "compute": svc_hdlr_compute,
        "object-store": svc_hdlr_obj_store}

