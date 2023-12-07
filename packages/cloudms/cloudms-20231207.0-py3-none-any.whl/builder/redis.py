import os
import asyncio
import logging
import base64
import jinja2
from uuid import UUID
from pydantic import BaseModel

from common.config import config, zone_conf
from common import util
from common import validator
from cluster import Cluster
from db import db
from openstack.nova import Flavor


log = logging.getLogger("uvicorn")


class RedisObject(BaseModel):
    name: str
    cluster_size: int = 1
    spec_id: UUID
    subnet_id: UUID
    volume_size: int = 40


class RedisPost(BaseModel):
    cluster: RedisObject


class RedisPutObject(BaseModel):
    status: str = ""


class RedisPut(BaseModel):
    cluster: RedisPutObject


class Redis(Cluster):
    def __init__(self, token_pack):
        super().__init__(token_pack, res_name="cluster",
                table_name="redis_cluster")
        self.svc_path = os.getcwd()
        self.build_log = "/var/log/cms/redis-build.log"
        if "build-log" in config["redis"]:
            self.build_log = config["redis"]["build-log"]
        loader = jinja2.FileSystemLoader(f"{self.svc_path}/redis-template")
        self.j2_env = jinja2.Environment(trim_blocks=True,
                lstrip_blocks=True, loader=loader)

    async def rh_post(self, req_data):
        req = req_data[self.res_name]
        v = {"name": "name"}
        msg = validator.validate(req, v)
        if msg:
            return {"status": 400, "data": {"message": msg}}
        cluster_size = req["cluster_size"]
        if cluster_size == 6:
            cluster_size = 3
        if cluster_size not in [1, 3]:
            msg = f"Cluster size {cluster_size} is not supported!"
            return {"status": 400, "data": {"message": msg}}
        if req["volume_size"] > 5000:
            msg = f"Volume size has to be < 5000GB!"
            return {"status": 400, "data": {"message": msg}}
        spec_id = str(req["spec_id"])
        obj = await Flavor(self.token_pack).get_obj(spec_id)
        if not obj:
            msg = f"Spec {spec_id} not found!"
            return {"status": 400, "data": {"message": msg}}
        cluster = {"name": req["name"],
                "project_id": self.project_id,
                "cluster_size": cluster_size,
                "subnet_id": str(req["subnet_id"]),
                "status": "building"}
        await db.add(self.table_name, cluster)
        cluster["volume_size"] = req["volume_size"]
        cluster["spec_id"] = spec_id
        task = asyncio.create_task(self.task_create_cluster(cluster))
        task.add_done_callback(util.task_done_cb)
        return {"status": 202, "data": {self.res_name: {"id": cluster["id"]}}}

    async def rh_put(self, id, req_data):
        req = req_data[self.res_name]
        update = {}
        if req["status"]:
            update["status"] = req["status"]
        await db.update(self.table_name, id, update)
        return {"status": 200}

    async def rh_delete(self, id):
        cluster = await self.get_obj(id)
        if not cluster:
            return {"status": 404}
        await db.update(self.table_name, id, {"status": "deleting"})
        task = asyncio.create_task(self.task_delete_cluster(cluster))
        task.add_done_callback(util.task_done_cb)
        return {"status": 202, "data": {self.res_name: {"id": id}}}

    async def task_create_cluster(self, cluster):
        cluster_id = cluster["id"]
        status_error = {"status": "error"}
        cluster["type"] = "redis"
        cluster["table"] = self.table_name
        cluster["image_name"] = config["redis"]["node-image"]
        log.info(f"Task create Redis cluster {cluster_id}.")
        if await self.create_cluster(cluster, enable_vip=False):
            await db.update(self.table_name, cluster_id, status_error)
            return
        update = {"service_address": cluster["service_address"]}
        await db.update(self.table_name, cluster_id, update)
        if await self.provision_cluster(cluster):
            await db.update(self.table_name, cluster_id, status_error)
        else:
            await db.update(self.table_name, cluster_id, {"status": "active"})
        log.info(f"Task create Redis cluster {cluster_id} is done.")

    async def task_delete_cluster(self, cluster):
        cluster_id = cluster["id"]
        status_error = {"status": "error"}
        cluster["type"] = "redis"
        cluster["table"] = self.table_name
        log.info(f"Task delete Redis cluster {cluster_id}.")
        if await self.delete_cluster(cluster):
            await db.update(self.table_name, cluster_id, status_error)
            return
        update = {"status": "deleted", "deleted": True}
        await db.update(self.table_name, cluster_id, update)
        log.info(f"Task delete Redis cluster {cluster_id} is done.")

    async def provision_cluster(self, cluster):
        cluster_id = cluster["id"]
        log.info(f"Provision node for Redis cluster {cluster_id}.")
        try:
            if os.stat(self.build_log).st_size > (1024 * 1024 * 1024):
                os.truncate(self.build_log, 0)
        except:
            pass
        await util.exec_cmd(f"mkdir -p /tmp/{cluster_id}")
        vars = {"service_proxy": config["DEFAULT"]["service-proxy"],
                "repo_baseos": config["repo"]["baseos"],
                "repo_appstream": config["repo"]["appstream"]}
        t = self.j2_env.get_template(f"depot.repo.j2")
        with open(f"/tmp/{cluster_id}/depot.repo", "w") as fd:
            fd.write(t.render(vars))
        orig_nodes = await db.get("cluster_instance",
                {"cluster_id": cluster_id})
        nodes = sorted(orig_nodes, key=lambda d: d["instance_name"])
        enable_cluster = "no"
        if cluster["cluster_size"] > 1:
            enable_cluster = "yes"
        for node in nodes:
            vars = {"node_address": node["user_address"],
                    "port": 6379,
                    "role": "master",
                    "enable_cluster": enable_cluster}
            t = self.j2_env.get_template(f"redis.conf.j2")
            with open(f"/tmp/{cluster_id}/redis-master.conf", "w") as fd:
                fd.write(t.render(vars))
            vars = {"node_address": node["user_address"],
                    "port": 6378,
                    "role": "slave",
                    "enable_cluster": enable_cluster}
            t = self.j2_env.get_template(f"redis.conf.j2")
            with open(f"/tmp/{cluster_id}/redis-slave.conf", "w") as fd:
                fd.write(t.render(vars))
            cmd = f"{self.svc_path}/redisadm deploy" \
                    f" {node['mgmt_address']} {cluster_id}"
            with open(self.build_log, "a") as fd:
                rc = await util.exec_cmd(cmd, output_file=fd)
            if rc:
                log.error(f"Deploy node failed!")
                return rc

        if cluster["cluster_size"] > 1:
            log.info(f"Bootstrap Redis cluster {cluster_id}.")
            addrs_str = ",".join([node["user_address"] for node in nodes])
            cmd = f"{self.svc_path}/redisadm bootstrap" \
                    f" {nodes[0]['mgmt_address']} {cluster_id}" \
                    f" {addrs_str}"
            with open(self.build_log, "a") as fd:
                rc = await util.exec_cmd(cmd, output_file=fd)
            if rc:
                log.error(f"Bootstrap cluster failed!")
                return rc
        await util.exec_cmd(f"rm -fr /tmp/{cluster_id}")

