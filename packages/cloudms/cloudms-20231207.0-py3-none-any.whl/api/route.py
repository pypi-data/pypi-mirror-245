import logging
from fastapi import FastAPI, WebSocket
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

import api
from common import config
from openstack.keystone import Auth

from router.message_queue import router_msg_q
from router.object_store import router_object_store	
from router.kubernetes import router_kubernetes
from router.cloudshell import router_cloudshell
from router.identity import router_identity
from router.network import router_network
from router.compute import router_compute 
from router.builder import router_builder
from router.monitor import router_monitor
from router.database import router_db 
from router.image import router_image 
from router.block import router_block 
from router.plan import router_plan 

log = logging.getLogger("uvicorn")
app = FastAPI()

app.include_router(router_object_store)	
app.include_router(router_kubernetes)
app.include_router(router_cloudshell)
app.include_router(router_identity)
app.include_router(router_network)
app.include_router(router_compute)
app.include_router(router_builder)
app.include_router(router_monitor)
app.include_router(router_image)
app.include_router(router_block)
app.include_router(router_msg_q)
app.include_router(router_plan)
app.include_router(router_db)


@app.on_event("startup")
async def api_start():
    log.info("Start server.")
    config.svc_token_pack = await Auth().get_svc_token(config.zone_conf)
    if config.svc_token_pack:
        log.info("Got service token.")
    else:
        log.error("Failed to get service token!")


@app.on_event("shutdown")
async def api_shutdown():
    log.info("Shutdown server.")


@app.get("/health")
async def get_health():
    return api.get_health()


@app.get("/config")
async def get_config():
    return api.get_config()


# kubernetes: cluster
@app.get("/v1/kubernetes/cluster")
async def get_kubernetes_clusters(req: Request):
    fwd_path = f"/kubernetes/cluster"
    return await api.op_api(req, "get", "cms-builder", fwd_path)


@app.get("/v1/kubernetes/cluster/{id}")
async def get_kubernetes_cluster(req: Request, id: str):
    fwd_path = f"/kubernetes/cluster/{id}"
    return await api.op_api(req, "get", "cms-builder", fwd_path)


@app.post("/v1/kubernetes/cluster")
async def post_kubernetes_cluster(req: Request):
    fwd_path = "/kubernetes/cluster"
    return await api.op_api(req, "post", "cms-builder", fwd_path)


@app.put("/v1/kubernetes/cluster/{id}")
async def put_kubernetes_cluster(req: Request, id: str):
    fwd_path = f"/kubernetes/cluster/{id}"
    return await api.op_api(req, "put", "cms-builder", fwd_path)


@app.delete("/v1/kubernetes/cluster/{id}")
async def delete_kubernetes_cluster(req: Request, id: str):
    fwd_path = f"/kubernetes/cluster/{id}"
    return await api.op_api(req, "delete", "cms-builder", fwd_path)


# cloudshell
@app.websocket("/v1/cloudshell/connect/{port}")
async def ws_connect_port(ws: WebSocket, port: str):
    fwd_path = f"/cloudshell/connect/{port}"
    return await api.websocket_bridge(ws, fwd_path)


app.mount("/v1/cloudshell/static", 
    StaticFiles(directory="../cloudshell/static", html=True), name="static")


@app.get("/{path_name:path}")
async def get_all(req: Request):
    return api.get_portal(req.url.path)

