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
from openstack.nova import Flavor, Instance
from openstack.cinder import Volume


log = logging.getLogger("uvicorn")


class NFSObject(BaseModel):
    name: str
    cluster_size: int = 1
    spec_id: UUID
    subnet_id: UUID


class NFSPost(BaseModel):
    cluster: NFSObject


class NFSPutObject(BaseModel):
    status: str = ""


class NFSPut(BaseModel):
    cluster: NFSPutObject


class DirectoryObject(BaseModel):
    name: str
    size: int


class NFSDirectoryPost(BaseModel):
    directory: DirectoryObject


class NFS(Cluster):
    def __init__(self, token_pack):
        super().__init__(token_pack, res_name="cluster",
                table_name="nfs_cluster")
        self.svc_path = os.getcwd()
        self.build_log = "/var/log/cms/nfs-build.log"
        if "build-log" in config["nfs"]:
            self.build_log = config["nfs"]["build-log"]
        loader = jinja2.FileSystemLoader(f"{self.svc_path}/nfs-template")
        self.j2_env = jinja2.Environment(trim_blocks=True,
                lstrip_blocks=True, loader=loader)

    async def rh_post(self, req_data):
        req = req_data[self.res_name]
        v = {"name": "name"}
        msg = validator.validate(req, v)
        if msg:
            return {"status": 400, "data": {"message": msg}}
        cluster_size = req["cluster_size"]
        if cluster_size not in [1, 2]:
            msg = f"Cluster size {cluster_size} is not supported!"
            return {"status": 400, "data": {"message": msg}}
        spec_id = str(req["spec_id"])
        obj = await Flavor(self.token_pack).get_obj(spec_id)
        if not obj:
            msg = f"Spec {spec_id} not found!"
            return {"status": 400, "data": {"message": msg}}
        cluster = {"name": req["name"],
                "project_id": self.project_id,
                "subnet_id": str(req["subnet_id"]),
                "cluster_size": cluster_size,
                "status": "building"}
        await db.add(self.table_name, cluster)
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

    async def rh_get_directory(self, cid):
        dirs = await db.get("nfs_directory", {"cluster_id": cid})
        return {"status": 202, "data": {"directorys": dirs}}

    async def rh_post_directory(self, cid, req_data):
        req = req_data["directory"]
        v = {"name": "name", "size": "size-volume"}
        msg = validator.validate(req, v)
        if msg:
            return {"status": 400, "data": {"message": msg}}
        cluster = await self.get_obj(cid)
        if cluster["status"] != "active":
            return {"status": 400, "data": {
                    "message": f"NFS cluster is not active!"}}
        dirs = await db.get("nfs_directory", {"cluster_id": cid})
        if len(dirs) >= 8:
            return {"status": 400, "data": {
                    "message": f"Exceed max 8 directories!"}}
        for dir in dirs:
            if dir["name"] == req["name"]:
                return {"status": 400, "data": {
                        "message": f"Directory {req['name']} exists!"}}
            if dir["status"] != "active":
                return {"status": 400, "data": {
                        "message": f"Directory {dir['name']} is not active!"}}
        dir = {"name": req["name"],
                "size": req["size"],
                "cluster_id": cid,
                "status": "building"}
        await db.add("nfs_directory", dir)
        task = asyncio.create_task(self.task_add_directory(dir, cluster))
        task.add_done_callback(util.task_done_cb)
        return {"status": 202, "data": {"directory": {"id": dir["id"]}}}

    async def rh_delete_directory(self, cid, name):
        v = {"name": "name"}
        msg = validator.validate({"name": name}, v)
        if msg:
            return {"status": 400, "data": {"message": msg}}
        cluster = await self.get_obj(cid)
        if not cluster:
            return {"status": 404}
        if (cluster["status"] != "active") and (cluster["status"] != "error"):
            msg = f"NFS cluster is {cluster['status']}, not active or error!"
            return {"status": 400, "data": {"message": msg}}
        dirs = await db.get("nfs_directory", {"cluster_id": cid})
        dir = None
        for dir_tmp in dirs:
            if dir_tmp["name"] == name:
                dir = dir_tmp
            if (dir_tmp["status"] != "active") \
                    and (dir_tmp["status"] != "error"):
                msg = f"Directory {dir_tmp['name']} is not active or error!"
                return {"status": 400, "data": {"message": msg}}
        if not dir:
            return {"status": 404, "data": {
                    "message": f"Directory {name} not found!"}}
        await db.update("nfs_directory", dir["id"], {"status": "deleting"})
        task = asyncio.create_task(self.task_remove_directory(dir, cluster))
        task.add_done_callback(util.task_done_cb)
        return {"status": 202}

    async def task_create_cluster(self, cluster):
        cluster_id = cluster["id"]
        status_error = {"status": "error"}
        cluster["type"] = "nfs"
        cluster["table"] = self.table_name
        cluster["image_name"] = config["nfs"]["node-image"]
        log.info(f"Task create NFS cluster {cluster_id}.")
        if await self.create_cluster(cluster):
            await db.update(self.table_name, cluster_id, status_error)
            return

        update = {"service_address": cluster["service_address"]}
        await db.update(self.table_name, cluster_id, update)

        if await self.provision_cluster(cluster):
            await db.update(self.table_name, cluster_id, status_error)
        else:
            await db.update(self.table_name, cluster_id, {"status": "active"})
        log.info(f"Task create NFS cluster {cluster_id} is done.")

    async def task_delete_cluster(self, cluster):
        cluster_id = cluster["id"]
        status_error = {"status": "error"}
        cluster["type"] = "nfs"
        cluster["table"] = self.table_name
        log.info(f"Task delete NFS cluster {cluster_id}.")

        dirs = await db.get("nfs_directory", {"cluster_id": cluster_id})
        for dir in dirs:
            await self.task_remove_directory(dir, cluster)

        if await self.delete_cluster(cluster):
            await db.update(self.table_name, cluster_id, status_error)
            return

        update = {"status": "deleted", "deleted": True}
        await db.update(self.table_name, cluster_id, update)
        log.info(f"Task delete NFS cluster {cluster_id} is done.")

    async def task_add_directory(self, dir, cluster):
        cluster_id = cluster["id"]
        status_error = {"status": "error"}
        log.info(f"Task add directory {dir['name']} to {cluster_id}.")
        vol_ins = Volume(self.token_pack)
        vol_name = f"nfs_{cluster['name']}_{dir['name']}"
        log.info(f"Create volume {vol_name}.")
        params = {"name": vol_name,
                "size": dir["size"],
                "volume_type": "gold"}
        if cluster["cluster_size"] > 1:
            params["volume_type"] = "gold-multi-attach"
        resp = await vol_ins.post({"volume": params})
        if resp["status"] != 202:
            log.error("Create volume {} failed! {}".format(
                    vol_name, resp["data"]))
            await db.update("nfs_directory", dir["id"], status_error)
            return
        vol_id = resp["data"]["volume"]["id"]

        if await self.wait_for_ready(vol_ins, [vol_id], "available"):
            await db.update("nfs_directory", dir["id"], status_error)
            return

        ins_ins = Instance(self.token_pack)
        nodes = await db.get("cluster_instance", {"cluster_id": cluster_id})
        for node in nodes:
            log.info(f"Attach volume {vol_id} to {node['instance_id']}.")
            data = {"volumeAttachment": {"volumeId": vol_id}}
            resp = await ins_ins.add_volume(node["instance_id"], data)
            if resp["status"] != 200:
                log.error("Attach volume {} to {} failed! {}".format(
                        vol_id, node["instance_id"], resp["data"]))
                await db.update("nfs_directory", dir["id"], status_error)
                return
            # In case of multi-attach, volume status is "reserved" right after
            # attach, need to wait till "in-use" when the attachment is
            # completed, before doing the next attachment.
            if await self.wait_for_ready(vol_ins, [vol_id], "in-use"):
                await db.update("nfs_directory", dir["id"], status_error)
                return
        try:
            if os.stat(self.build_log).st_size > (1024 * 1024 * 1024):
                os.truncate(self.build_log, 0)
        except:
            pass
        for node in nodes:
            cmd = f"{self.svc_path}/nfsadm add-directory" \
                    f" {node['mgmt_address']} {cluster_id} {dir['name']}" \
                    f" {vol_id[:18]}"
            with open(self.build_log, "a") as fd:
                rc = await util.exec_cmd(cmd, output_file=fd)
            if rc:
                log.error(f"Add directory failed!")
                await db.update("nfs_directory", dir["id"], status_error)
                return rc
        update = {"status": "active", "volume_id": vol_id}
        await db.update("nfs_directory", dir["id"], update)
        log.info(f"Task add directory {dir['name']} to {cluster_id} is done.")

    async def task_remove_directory(self, dir, cluster):
        cluster_id = cluster["id"]
        status_error = {"status": "error"}
        log.info(f"Task remove directory {dir['name']} from {cluster_id}.")
        nodes = await db.get("cluster_instance", {"cluster_id": cluster_id})
        try:
            if os.stat(self.build_log).st_size > (1024 * 1024 * 1024):
                os.truncate(self.build_log, 0)
        except:
            pass
        for node in nodes:
            cmd = f"{self.svc_path}/nfsadm remove-directory" \
                    f" {node['mgmt_address']} {cluster_id} {dir['name']}"
            with open(self.build_log, "a") as fd:
                rc = await util.exec_cmd(cmd, output_file=fd)

        ins_ins = Instance(self.token_pack)
        vol_ins = Volume(self.token_pack)
        vol_id = dir["volume_id"]
        for node in nodes:
            log.info(f"Detach volume {vol_id} from {node['instance_id']}.")
            resp = await ins_ins.remove_volume(node["instance_id"], vol_id)
            if resp["status"] != 202:
                log.error("Detach volume {} from {} failed! {}".format(
                        vol_id, node["instance_id"], resp["data"]))
            # In case of multi-attach, volume status is "detaching" right
            # after detach, need to wait till "in-use" when the detachment is
            # completed, before doing the next detachment. After the
            # last detachment, the status will be "available".
            status = "in-use"
            if nodes.index(node) == len(nodes) - 1:
                status = "available"
            if await self.wait_for_ready(vol_ins, [vol_id], status):
                await db.update("nfs_directory", dir["id"], status_error)

        log.info(f"Delete volume {vol_id}.")
        resp = await vol_ins.delete(vol_id)
        if resp["status"] != 202:
            log.error("Delete volume {} failed! {}".format(
                    vol_id, resp["data"]))
        await db.delete("nfs_directory", dir["id"])
        log.info(f"Task remove directory {dir['name']} from {cluster_id}"
                " is done.")

    async def provision_cluster(self, cluster):
        cluster_id = cluster["id"]
        log.info(f"Provision node for NFS cluster {cluster_id}.")
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
        if cluster["cluster_size"] > 1:
            vars = {"vip": cluster["service_address"],
                    "vrid": cluster["service_address"].split(".")[-1]}
            t = self.j2_env.get_template(f"keepalived.conf.j2")
            with open(f"/tmp/{cluster_id}/keepalived.conf", "w") as fd:
                fd.write(t.render(vars))
        nodes = await db.get("cluster_instance", {"cluster_id": cluster_id})
        for node in nodes:
            cmd = f"{self.svc_path}/nfsadm deploy {node['mgmt_address']}" \
                    f" {cluster_id} {cluster['cluster_size'] > 1}"
            with open(self.build_log, "a") as fd:
                rc = await util.exec_cmd(cmd, output_file=fd)
            if rc:
                log.error(f"Provision node failed!")
                return rc
        await util.exec_cmd(f"rm -fr /tmp/{cluster_id}")

