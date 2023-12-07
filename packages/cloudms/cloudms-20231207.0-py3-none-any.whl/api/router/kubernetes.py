from fastapi import APIRouter
from fastapi.requests import Request

import api

router_kubernetes = APIRouter(prefix="/v1/kubernetes", tags=["kubernetes"])


@router_kubernetes.get("")
async def get_kubernetess(req: Request):
    fwd_path = "/kubernetes"
    return await api.op_api(req, "get", "cms-builder", fwd_path)


@router_kubernetes.post("")
async def post_kubernetes(req: Request):
    fwd_path = "/kubernetes"
    return await api.op_api(req, "post", "cms-builder", fwd_path)


@router_kubernetes.get("/{id}")
async def get_kubernetes(req: Request, id: str):
    fwd_path = f"/kubernetes/{id}"
    return await api.op_api(req, "get", "cms-builder", fwd_path)


@router_kubernetes.put("/{id}")
async def put_kubernetes(req: Request, id: str):
    fwd_path = f"/kubernetes/{id}"
    return await api.op_api(req, "put", "cms-builder", fwd_path)


@router_kubernetes.delete("/{id}")
async def delete_kubernetes(req: Request, id: str):
    fwd_path = f"/kubernetes/{id}"
    return await api.op_api(req, "delete", "cms-builder", fwd_path)


@router_kubernetes.get("/{id}/config")
async def get_kubernetes_config(req: Request, id: str):
    fwd_path = f"/kubernetes/{id}/config"
    return await api.op_api(req, "get", "cms-builder", fwd_path)


@router_kubernetes.get("/{id}/worker")
async def get_kubernetes_worker(req: Request, id: str):
    fwd_path = f"/kubernetes/{id}/worker"
    return await api.op_api(req, "get", "cms-builder", fwd_path)


@router_kubernetes.post("/{id}/worker")
async def post_kubernetes_worker(req: Request, id: str):
    fwd_path = f"/kubernetes/{id}/worker"
    return await api.op_api(req, "post", "cms-builder", fwd_path)

