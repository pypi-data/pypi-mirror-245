import asyncio
import logging
from fastapi import FastAPI, Header

from common import util, config
from common.route_wrapper import route_wrapper
from openstack.keystone import Auth
from db import db
from nfs import NFS, NFSPost, NFSPut, NFSDirectoryPost
from k8s import K8s, K8sPost, K8sPut, K8sWorkerPost
from mariadb import MariaDB, MariaDBPost, MariaDBPut
from postgresql import PostgreSQL, PostgreSQLPost, PostgreSQLPut
from redis import Redis, RedisPost, RedisPut
from rabbitmq import RabbitMQ, RabbitMQPost, RabbitMQPut
from kafka import Kafka, KafkaPost, KafkaPut

log = logging.getLogger("uvicorn")
app = FastAPI()


@app.on_event("startup")
async def api_start():
    log.info("Start server.")
    await db.create_engine()
    rc = await db.check_table()
    while rc:
        log.error(f"Failed to check DB! Retry.")
        await asyncio.sleep(10)
        rc = await db.check_table()
    config.svc_token_pack = await Auth().get_svc_token(config.zone_conf)
    if config.svc_token_pack:
        log.info("Got service token.")
    else:
        log.error("Failed to get service token!")


@app.on_event("shutdown")
async def api_shutdown():
    log.info("Shutdown server.")


@app.get("/")
async def get_root():
    return {"message": util.msg_root}


'''
NFS Cluster
'''


@app.get("/v1/nfs")
@route_wrapper
async def get_nfs_list(
        x_auth_token=Header(None), token_pack=None,
        all_projects: bool = True, name: str = None):
    return await NFS(token_pack).rh_get_list(query={"name": name})


@app.get("/v1/nfs/{id}")
@route_wrapper
async def get_nfs(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await NFS(token_pack).rh_get(id)


@app.get("/v1/nfs/{id}/instance")
@route_wrapper
async def get_nfs_instance(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await NFS(token_pack).rh_get_instance(id)


@app.post("/v1/nfs")
@route_wrapper
async def post_nfs(req: NFSPost,
        x_auth_token=Header(None), token_pack=None):
    return await NFS(token_pack).rh_post(req.dict())


@app.put("/v1/nfs/{id}")
@route_wrapper
async def put_nfs(id: str, req: NFSPut,
        x_auth_token=Header(None), token_pack=None):
    return await NFS(token_pack).rh_put(id, req.dict())


@app.delete("/v1/nfs/{id}")
@route_wrapper
async def delete_nfs(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await NFS(token_pack).rh_delete(id)


'''
NFS Directory
'''


@app.get("/v1/nfs/{cid}/directory")
@route_wrapper
async def get_nfs_directory_list(cid: str,
        x_auth_token=Header(None), token_pack=None):
    return await NFS(token_pack).rh_get_directory(cid)


@app.post("/v1/nfs/{cid}/directory")
@route_wrapper
async def post_nfs_directory(cid: str, req: NFSDirectoryPost,
        x_auth_token=Header(None), token_pack=None):
    return await NFS(token_pack).rh_post_directory(cid, req.dict())


@app.delete("/v1/nfs/{cid}/directory/{name}")
@route_wrapper
async def delete_nfs_directory(cid: str, name: str,
        x_auth_token=Header(None), token_pack=None):
    return await NFS(token_pack).rh_delete_directory(cid, name)


'''
Kubernetes Cluster
'''


@app.get("/v1/kubernetes")
@route_wrapper
async def get_k8s_list(
        x_auth_token=Header(None), token_pack=None,
        all_projects: bool = True, name: str = None):
    return await K8s(token_pack).rh_get_list(query={"name": name})


@app.get("/v1/kubernetes/{id}")
@route_wrapper
async def get_k8s(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await K8s(token_pack).rh_get(id)


@app.post("/v1/kubernetes")
@route_wrapper
async def post_k8s(req: K8sPost,
        x_auth_token=Header(None), token_pack=None):
    return await K8s(token_pack).rh_post(req.dict())


@app.put("/v1/kubernetes/{id}")
@route_wrapper
async def put_k8s(id: str, req: K8sPut,
        x_auth_token=Header(None), token_pack=None):
    return await K8s(token_pack).rh_put(id, req.dict())


@app.delete("/v1/kubernetes/{id}")
@route_wrapper
async def delete_k8s(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await K8s(token_pack).rh_delete(id)


'''
Kubernetes config
'''


@app.get("/v1/kubernetes/{id}/config")
@route_wrapper
async def get_k8s_config(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await K8s(token_pack).rh_get_config(id)


'''
Kubernetes Worker
'''


@app.get("/v1/kubernetes/{id}/worker")
@route_wrapper
async def get_k8s_worker_list(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await K8s(token_pack).rh_get_worker(id)


@app.post("/v1/kubernetes/{id}/worker")
@route_wrapper
async def post_k8s_worker(id: str, req: K8sWorkerPost,
        x_auth_token=Header(None), token_pack=None):
    return await K8s(token_pack).rh_post_worker(id, req.dict())


'''
MariaDB Cluster
'''
@app.get("/v1/mariadb")
@route_wrapper
async def get_maria_list(
        x_auth_token=Header(None), token_pack=None,
        all_projects: bool = True, name: str = None):
    return await MariaDB(token_pack).rh_get_list(query={"name": name})


@app.get("/v1/mariadb/{id}")
@route_wrapper
async def get_mariadb(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await MariaDB(token_pack).rh_get(id)


@app.get("/v1/mariadb/{id}/instance")
@route_wrapper
async def get_mariadb_instance(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await MariaDB(token_pack).rh_get_instance(id)


@app.post("/v1/mariadb")
@route_wrapper
async def post_mariadb(req: MariaDBPost,
        x_auth_token=Header(None), token_pack=None):
    return await MariaDB(token_pack).rh_post(req.dict())


@app.put("/v1/mariadb/{id}")
@route_wrapper
async def put_mariadb(id: str, req: MariaDBPut,
        x_auth_token=Header(None), token_pack=None):
    return await MariaDB(token_pack).rh_put(id, req.dict())


@app.delete("/v1/mariadb/{id}")
@route_wrapper
async def delete_mariadb(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await MariaDB(token_pack).rh_delete(id)


'''
PostgreSQL Cluster
'''
@app.get("/v1/postgresql")
@route_wrapper
async def get_maria_list(
        x_auth_token=Header(None), token_pack=None,
        all_projects: bool = True, name: str = None):
    return await PostgreSQL(token_pack).rh_get_list(query={"name": name})


@app.get("/v1/postgresql/{id}")
@route_wrapper
async def get_postgresql(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await PostgreSQL(token_pack).rh_get(id)


@app.get("/v1/postgresql/{id}/instance")
@route_wrapper
async def get_postgresql_instance(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await PostgreSQL(token_pack).rh_get_instance(id)


@app.post("/v1/postgresql")
@route_wrapper
async def post_postgresql(req: PostgreSQLPost,
        x_auth_token=Header(None), token_pack=None):
    return await PostgreSQL(token_pack).rh_post(req.dict())


@app.put("/v1/postgresql/{id}")
@route_wrapper
async def put_postgresql(id: str, req: PostgreSQLPut,
        x_auth_token=Header(None), token_pack=None):
    return await PostgreSQL(token_pack).rh_put(id, req.dict())


@app.delete("/v1/postgresql/{id}")
@route_wrapper
async def delete_postgresql(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await PostgreSQL(token_pack).rh_delete(id)


'''
Redis Cluster
'''
@app.get("/v1/redis")
@route_wrapper
async def get_maria_list(
        x_auth_token=Header(None), token_pack=None,
        all_projects: bool = True, name: str = None):
    return await Redis(token_pack).rh_get_list(query={"name": name})


@app.get("/v1/redis/{id}")
@route_wrapper
async def get_redis(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await Redis(token_pack).rh_get(id)


@app.get("/v1/redis/{id}/instance")
@route_wrapper
async def get_redis_instance(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await Redis(token_pack).rh_get_instance(id)


@app.post("/v1/redis")
@route_wrapper
async def post_redis(req: RedisPost,
        x_auth_token=Header(None), token_pack=None):
    return await Redis(token_pack).rh_post(req.dict())


@app.put("/v1/redis/{id}")
@route_wrapper
async def put_redis(id: str, req: RedisPut,
        x_auth_token=Header(None), token_pack=None):
    return await Redis(token_pack).rh_put(id, req.dict())


@app.delete("/v1/redis/{id}")
@route_wrapper
async def delete_redis(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await Redis(token_pack).rh_delete(id)


'''
RabbitMQ Cluster
'''
@app.get("/v1/rabbitmq")
@route_wrapper
async def get_maria_list(
        x_auth_token=Header(None), token_pack=None,
        all_projects: bool = True, name: str = None):
    return await RabbitMQ(token_pack).rh_get_list(query={"name": name})


@app.get("/v1/rabbitmq/{id}")
@route_wrapper
async def get_rabbitmq(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await RabbitMQ(token_pack).rh_get(id)


@app.get("/v1/rabbitmq/{id}/instance")
@route_wrapper
async def get_rabbitmq_instance(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await RabbitMQ(token_pack).rh_get_instance(id)


@app.post("/v1/rabbitmq")
@route_wrapper
async def post_rabbitmq(req: RabbitMQPost,
        x_auth_token=Header(None), token_pack=None):
    return await RabbitMQ(token_pack).rh_post(req.dict())


@app.put("/v1/rabbitmq/{id}")
@route_wrapper
async def put_rabbitmq(id: str, req: RabbitMQPut,
        x_auth_token=Header(None), token_pack=None):
    return await RabbitMQ(token_pack).rh_put(id, req.dict())


@app.delete("/v1/rabbitmq/{id}")
@route_wrapper
async def delete_rabbitmq(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await RabbitMQ(token_pack).rh_delete(id)


'''
Kafka Cluster
'''
@app.get("/v1/kafka")
@route_wrapper
async def get_maria_list(
        x_auth_token=Header(None), token_pack=None,
        all_projects: bool = True, name: str = None):
    return await Kafka(token_pack).rh_get_list(query={"name": name})


@app.get("/v1/kafka/{id}")
@route_wrapper
async def get_kafka(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await Kafka(token_pack).rh_get(id)


@app.get("/v1/kafka/{id}/instance")
@route_wrapper
async def get_kafka_instance(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await Kafka(token_pack).rh_get_instance(id)


@app.post("/v1/kafka")
@route_wrapper
async def post_kafka(req: KafkaPost,
        x_auth_token=Header(None), token_pack=None):
    return await Kafka(token_pack).rh_post(req.dict())


@app.put("/v1/kafka/{id}")
@route_wrapper
async def put_kafka(id: str, req: KafkaPut,
        x_auth_token=Header(None), token_pack=None):
    return await Kafka(token_pack).rh_put(id, req.dict())


@app.delete("/v1/kafka/{id}")
@route_wrapper
async def delete_kafka(id: str,
        x_auth_token=Header(None), token_pack=None):
    return await Kafka(token_pack).rh_delete(id)

