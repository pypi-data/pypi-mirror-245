from fastapi import APIRouter
from fastapi.requests import Request

import api

router_msg_q = APIRouter(prefix="/v1/message-queue", tags=["message-queue"])


''' 
RabbitMQ
'''

@router_msg_q.get("/rabbitmq")
async def get_rabbitmq_list(req: Request):
    fwd_path = "/rabbitmq"
    return await api.op_api(req, "get", "cms-builder", fwd_path)


@router_msg_q.post("/rabbitmq")
async def post_rabbitmq(req: Request):
    fwd_path = "/rabbitmq"
    return await api.op_api(req, "post", "cms-builder", fwd_path)


@router_msg_q.get("/rabbitmq/{id}")
async def get_rabbitmq(req: Request, id: str):
    fwd_path = f"/rabbitmq/{id}"
    return await api.op_api(req, "get", "cms-builder", fwd_path)


@router_msg_q.get("/rabbitmq/{id}/instance")
async def get_rabbitmq_instance(req: Request, id: str):
    fwd_path = f"/rabbitmq/{id}/instance"
    return await api.op_api(req, "get", "cms-builder", fwd_path)


@router_msg_q.put("/rabbitmq/{id}")
async def put_rabbitmq(req: Request, id: str):
    fwd_path = f"/rabbitmq/{id}"
    return await api.op_api(req, "put", "cms-builder", fwd_path)


@router_msg_q.delete("/rabbitmq/{id}")
async def delete_rabbitmq(req: Request, id: str):
    fwd_path = f"/rabbitmq/{id}"
    return await api.op_api(req, "delete", "cms-builder", fwd_path)

