import asyncio
from datetime import datetime
import os
import hashlib
import logging
import json
import aiohttp
from fastapi import Response
import traceback

log = logging.getLogger("uvicorn")

msg_root = "Active."
id_zero = "00000000-0000-0000-0000-000000000000"
time_format_iso = "%Y-%m-%dT%H:%M:%S"


def get_time():
    return datetime.now().strftime(time_format_iso)


def pop_none(d):
    for key in list(d.keys()):
        if type(d[key]) is dict:
            pop_none(d[key])
        elif d[key] is None:
            d.pop(key)


def get_q_str(query):
    q = ""
    if query:
        for key in query.keys():
            if query[key]:
                if not q:
                    q += f"?{key}={query[key]}"
                else:
                    q += f"&{key}={query[key]}"
    return q


def get_svc_url(catalog, service):
    url = None
    for svc in catalog:
        if svc["type"] == service:
            for ep in svc["endpoints"]:
                if ep["interface"] == "public":
                    url = ep["url"]
                    break
            break
    return url


def get_file_hash(name):
    file_key = "{}:{}".format(name, os.stat(name).st_mtime)
    (md5, sha256) = (None, None)
    with open(name, 'rb') as f:
        (md5, sha256) = calculate_hashe(f)
    return md5, sha256


def calculate_hashe(data):
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    if hasattr(data, "read"):
        for chunk in iter(lambda: data.read(8192), b""):
            md5.update(chunk)
            sha256.update(chunk)
    else:
        md5.update(data)
        sha256.update(data)
    return md5.hexdigest(), sha256.hexdigest()


async def send_req(op, url, headers, data=None, type_json=True):
    #log.debug(f"Send request {op} {url}")
    #log.debug(f"Send request headers: {headers}")
    #log.debug(f"Send request data: {data}")
    req_data = None
    resp_status = 500
    resp_headers = {}
    resp_dict = None
    if data:
        data_type = type(data)
        if (data_type is dict) or (data_type is list):
            req_data = json.dumps(data).encode("utf-8")
        elif (data_type is bytes) or (data_type is str):
            req_data = data
        else:
            log.error(f"Request data type {data_type} is not supported!")
            return {"status": resp_status, "headers": resp_headers,
                    "data": resp_dict}
    async with aiohttp.ClientSession() as session:
        func = getattr(session, op)
        try:
            async with func(url, headers=headers, data=req_data, ssl=False) \
                    as resp:
                resp_data = await resp.read()
                if resp_data:
                    if type_json:
                        resp_data = json.loads(resp_data.decode("utf-8"))
            resp_status = resp.status
            resp_headers = resp.headers
            if resp_status >= 400:
                log.debug(f"Send request op: {op} url: {url} data: {data}")
                log.debug(f"send_req response: {resp_status} {resp_data}")
        except Exception as e:
            log.error(f"Exception: {e}, {op}, {url}")
    return {"status": resp_status, "data": resp_data, "headers": resp_headers}


def response(status, headers=None, data=None):
    resp_data = None
    if data is not None:
        data_type = type(data)
        if (data_type is dict) or (data_type is list):
            resp_data = json.dumps(data).encode("utf-8")
        elif (data_type is bytes) or (data_type is str):
            resp_data = data
        else:
            log.error(f"Response data type {data_type} is not supported!")
            return Response(status_code=500)
    return Response(status_code=status, headers=headers, content=resp_data)


async def exec_cmd(cmd, output=False, output_file=None):
    log.debug(f"Run \"{cmd}\".")
    if output_file:
        p = await asyncio.create_subprocess_shell(cmd,
                stdout=output_file, stderr=output_file)
        await p.wait()
    else:
        p = await asyncio.create_subprocess_shell(cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await p.communicate()
    if p.returncode == 0:
        if not output_file:
            log.debug(f"stdout: {stdout.decode().strip()}")
    else:
        if not output_file:
            log.debug(f"stderr: {stderr.decode().strip()}")
    if output:
        return p.returncode, stdout.decode().strip()
    else:
        return p.returncode


def task_done_cb(self):
    try:
        self.result()
    except Exception as e:
        log.error(traceback.format_exc())


def get_pool_by_volume_type(vol_type):
    map = {"__DEFAULT__": "volume",
           "gold": "volume-ssd",
           "gold-plus": "volume-ssd-raw",
           "silver": "volume-hybrid",
           "bronze": "volume-hdd"}
    if vol_type not in map.keys():
        log.error(f"Volume type {vol_type} is not supported!")
        return
    return map[vol_type]


def get_snapshot_spec(name, res_type, res_id, vol_id=None, vol_type=None):
    pool = None
    if vol_type:
        pool = get_pool_by_volume_type(vol_type)
        if not pool:
            return
    spec = None
    if res_type == "instance":
        if vol_id:
            spec = f"{pool}/volume-{vol_id}@{name}"
        else:
            spec = f"vm/{res_id}_disk@{name}"
    elif res_type == "volume":
        spec = f"{pool}/volume-{res_id}@{name}"
    else:
        log.error(f"Invalid resource type {res_type}!")
    return spec

