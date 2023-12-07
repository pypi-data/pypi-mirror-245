"""
Support Monitor Service for user project
"""
import asyncio
from datetime import datetime, timedelta
from jwcrypto import jwk, jwt
import jinja2
import json
import logging
import os
import secrets
import string

from common.config import config, zone_conf
from common.resource_base import ResourceBase
from common import util
from db import db
from openstack.glance import Image
from openstack.keystone import Auth
from openstack.neutron import FloatingIP, Network, Port, SecurityGroup,\
    Subnet, Router
from openstack.nova import Flavor, Instance


log = logging.getLogger("uvicorn")


class MonitorCluster(ResourceBase):

    def __init__(self, token_pack):
        super().__init__(token_pack, res_name="cluster")
        self.cluster_path = "/var/lib/cms/monitor"
        self.serv_path = "/usr/local/cms/monitor"
        self.config_log = "/var/log/cms/monitor-config.log"
        loader = jinja2.FileSystemLoader(f"{self.serv_path}/monitor-template")
        self.j2_env = jinja2.Environment(trim_blocks=True,
                lstrip_blocks=True, loader=loader)

    async def _create_subnet_port(self, res_id, network_id,
            subnet_id, sg_name):
        svc_token_pack = await Auth().get_svc_token(zone_conf)
        port = {"network_id": network_id,
                "fixed_ips": [{"subnet_id": subnet_id}]}
        # Get the security_group id at first
        if sg_name:
            sg_id = await self._get_resource_id_by_name(
                    SecurityGroup(svc_token_pack), sg_name)
            if not sg_id:
                update = {"status": "error"}
                await db.update(self.table_name, res_id, update)
                return
            port["security_groups"] = [sg_id]
        request_data = {"port": port}
        resp_data = await Port(svc_token_pack).post(request_data)
        if await self._check_resp_data(resp_data, 201, res_id,
                                      f"Create port from subnet failed!"):
            return
        resp_data = resp_data.get("data").get("port")
        ip = None
        if resp_data.get("fixed_ips"):
            ip = resp_data.get("fixed_ips")[0].get("ip_address")
        return {"port_id": resp_data.get("id"), "port_ip": ip}

    async def _associate_vip(self, res_id, req_data, network_id,
            subnet_id, sg_name, ports):
        # Create virtual ip port from subnet
        if req_data.get("cluster_size") == 1:
            for port in ports:
                return {"port_ip": port.get("port_ip"),
                        "port_id": port.get("port_id")}
        svc_token_pack = await Auth().get_svc_token(zone_conf)
        virtual_port_data = await self._create_subnet_port(res_id,
                network_id, subnet_id, sg_name)
        if not virtual_port_data:
            log.error(f"Create virtual ip failed!")
            return
        update = {}
        for port in ports:
            update["allowed_address_pairs"] = [{
                    "ip_address": virtual_port_data.get("port_ip")}]
            request_data = {"port": update}
            resp_data = await Port(svc_token_pack).put(port.get("port_id"),
                    request_data)
            if await self._check_resp_data(resp_data, 200, res_id,
                                          f"Update port for virtual failed!"):
                return
        return {"port_ip": virtual_port_data.get("port_ip"),
                "port_id": virtual_port_data.get("port_id")}

    @staticmethod
    def _get_config_values(req):
        for configure in ["node-spec", "node-image", "node-disk-size",
                          "svc-mgmt", "node-sg", "key-name"]:
            if configure == "svc-mgmt":
                if config['DEFAULT'][configure]:
                    req[configure] = config['DEFAULT'][configure]
                else:
                    req[configure] = "svc-mgmt"
            elif configure == "node-sg":
                if config["monitor"][configure]:
                    req[configure] = config['monitor'][configure]
                else:
                    req[configure] = "monitor-default"
            else:
                if config["monitor"][configure]:
                    req[configure] = config['monitor'][configure]
                else:
                    log.error(f"{configure} in conf file cannot be None.")
                    return False
        return True

    async def _associate_floating_ip(self, res_id, req_data, internal_address):
        svc_token_pack = await Auth().get_svc_token(zone_conf)
        floating_ip_address = req_data.get("service_address")
        # Get ports which device_owner is network:router_interface
        query = {"device_owner": "network:router_interface"}
        resp_data = await Port(svc_token_pack).get_list(query=query)
        if await self._check_resp_data(resp_data, 200, res_id,
                                      f"Query router interface failed!"):
            return
        router_id = None
        jump = False
        for port in resp_data.get("data").get("ports"):
            for fixed_ip in port.get("fixed_ips"):
                if fixed_ip.get("subnet_id") == req_data.get("subnet_id"):
                    router_id = port.get("device_id")
                    jump = True
                    break
            if jump:
                break
        if not router_id:
            update = {"status": "error"}
            await db.update(self.table_name, res_id, update)
            log.error(f"Can't find the router with external network!")
            return
        # Get the router info according to the router_id
        resp_data = await Router(self.token_pack).get(router_id)
        if await self._check_resp_data(resp_data, 200, res_id,
                f"Query router info failed!"):
            return
        router = resp_data.get("data").get("router")
        # Create the floating ip and associate it to virtual ip port
        floating_network_id = router.get(
                "external_gateway_info").get("network_id")
        floating_ip_data = {}
        if floating_ip_address:
            floating_ip_data["floating_ip_address"] = floating_ip_address
        floating_ip_data["floating_network_id"] = floating_network_id
        floating_ip_data["fixed_ip_address"] = internal_address.get("port_ip")
        floating_ip_data["port_id"] = internal_address.get("port_id")
        request_data = {"floatingip": floating_ip_data}
        resp_data = await FloatingIP(svc_token_pack).post(request_data)
        if await self._check_resp_data(resp_data, 201, res_id,
                f"Binding the floating ip failed!"):
            return
        resp_data = resp_data.get("data").get("floatingip")
        ext_ip = resp_data.get("floating_ip_address")
        ext_id = resp_data.get("id")
        external_address = {"ip": ext_ip, "id": ext_id}
        return external_address

    @staticmethod
    async def _get_resource_id_by_name(resource, res_ins_name):
        res_name = resource.res_name
        res_id = await resource.get_id_by_name(res_ins_name)
        if not res_id:
            log.error(f"Get {res_name} id by name {res_ins_name} failed!")
        return res_id

    async def _check_resp_data(self, resp_data, status, cluster_id,
                              error_message):
        if not resp_data or resp_data.get("status") != status:
            update = {"status": "error"}
            await db.update(self.table_name, cluster_id, update)
            log.error(error_message + f" Resp is {resp_data}")
            return True
        return False

    async def _wait_instances_ready(self, res_id, svc_token_pack,
           query, instance_ips):
        resp_data = await self.wait_for_batch_ready(
            Instance(svc_token_pack), query, "ACTIVE")
        if await self._check_resp_data(resp_data, 200, res_id,
                f"Get instances ready failed!"):
            return False
        for resp in resp_data.get("data"):
            port_info = list(resp.get("addresses").values())[0][0]
            ins_ip = port_info.get("addr")
            ins_mac = port_info.get("OS-EXT-IPS-MAC:mac_addr")
            query = {"mac_address": ins_mac}
            resp_port = await Port(svc_token_pack).get_list(query=query)
            if await self._check_resp_data(resp_port, 200, res_id,
                    f"Get fixed port id error"):
                return False
            ins_port_id = resp_port.get("data").get("ports")[0].get("id")
            instance_ips.append({"port_ip": ins_ip, "port_id": ins_port_id})
            update = {"fixed_address": ins_ip}
            await db.update("cluster_instance", resp.get("id"), update)
        update = {"status": "configuring"}
        await db.update(self.table_name, res_id, update)
        return True

    async def _batch_create_subnet_port(self, res_id, req_data, ports):
        subnet_id = req_data.get("subnet_id")
        sg_name = req_data.get("node-sg")
        resp_data = await Subnet(self.token_pack).get(subnet_id)
        if await self._check_resp_data(resp_data, 200, res_id,
                                       f"Get subnet information failed!"):
            return False
        resp_data = resp_data.get("data").get("subnet")
        req_data["user_network_id"] = resp_data.get("network_id")
        for x in range(req_data.get("cluster_size")):
            port_data = await self._create_subnet_port(res_id,
                    resp_data.get("network_id"), subnet_id, sg_name)
            if not port_data:
                return False
            ports.append(port_data)
        return True

    async def _attach_port_to_instance(self, res_id, svc_token_pack,
            ports, instance_ids):
        for instance_id in instance_ids:
            port = ports.pop()
            interface = {"port_id": port.get("port_id")}
            request_data = {"interfaceAttachment": interface}
            resp_data = await Instance(svc_token_pack).add_interface(
                instance_id, request_data)
            if await self._check_resp_data(resp_data, 200, res_id,
                    f"Attach port to server {instance_id} failed!"):
                return False
            update = {"port_address": port.get("port_ip"),
                      "port_id": port.get("port_id")}
            await db.update("cluster_instance", instance_id, update)
        return True

    async def _update_cluster_instance_db(self, res_id, svc_token_pack,
            query, instance_ids):
        reserved = query.get("reservation_id")
        resp_data = await Instance(svc_token_pack).get_list(query=query)
        if await self._check_resp_data(resp_data, 200, res_id,
                f"Get instance error"):
            return
        for resp in resp_data.get("data").get("servers"):
            instance_ids.append(resp.get("id"))
            instance = {"id": resp.get("id"), "reservation_id": reserved,
                        "cluster_id": res_id}
            await db.add("cluster_instance", instance)
        return resp_data

    async def task_config_cluster_server(self, res_id, req_data, reserved):
        # Update the DB
        svc_token_pack = await Auth().get_svc_token(zone_conf)
        query = {"reservation_id": reserved}
        instance_ids = []
        resp_data = await self._update_cluster_instance_db(res_id,
                svc_token_pack, query, instance_ids)
        if not resp_data:
            return
        # Wait for the instances are ready
        instance_ips = []
        result = await self._wait_instances_ready(res_id, svc_token_pack,
                query, instance_ips)
        if not result:
            return
        # Create virtual ip port for fixed ports
        net_id = await self._get_resource_id_by_name(
                Network(svc_token_pack), req_data.get("svc-mgmt"))
        network_data = await Network(svc_token_pack).get(net_id)
        network_data = network_data.get("data").get("network")
        instance_vip = await self._associate_vip(res_id, req_data,
                net_id, network_data["subnets"][0], None, instance_ips)
        if not instance_vip:
            return
        # Create ports for cluster servers
        ports = []
        result = await self._batch_create_subnet_port(res_id, req_data, ports)
        if not result:
            return
        # Create virtual ip port for user subnet ports
        external_address = await self._associate_vip(res_id, req_data,
                req_data.get("user_network_id"), req_data.get("subnet_id"),
                req_data.get("node-sg"), ports)
        if not external_address:
            return
        # Attach port to servers
        result = await self._attach_port_to_instance(res_id, svc_token_pack,
                ports, instance_ids)
        if not result:
            return
        # Update the db if everything is going well
        update = {"external_address": external_address.get("port_ip"),
                  "external_id":  external_address.get("port_id"),
                  "internal_address": instance_vip.get("port_ip"),
                  "internal_id": instance_vip.get("port_id")}
        await db.update(self.table_name, res_id, update)
        # Use script to ssh into cluster instances to config monitor portal
        data = {"monitor_username": req_data.get("monitor_username"),
                "monitor_password": req_data.get("monitor_password"),
                "monitor_org": req_data.get("monitor_username"),
                "internal_address": instance_vip.get("port_ip"),
                "external_address": external_address.get("port_ip"),
                "cluster_hosts": instance_ips}
        await self.task_config_monitor_portal(res_id, data)
        if req_data.get("cluster_size") > 1:
            await self.task_config_cluster_ha(res_id, data)

    async def task_create_cluster_server(self, req_data, res_id):
        log.info("Create cluster instance begin.")
        # Create cluster instances
        svc_token_pack = await Auth().get_svc_token(zone_conf)
        flavor_id = await self._get_resource_id_by_name(
                Flavor(svc_token_pack), req_data.get("node-spec"))
        net_id = await self._get_resource_id_by_name(
                Network(svc_token_pack), req_data.get("svc-mgmt"))
        image_id = await self._get_resource_id_by_name(
                Image(svc_token_pack), req_data.get("node-image"))
        server = {
                  "name": req_data.get("name"),
                  "min_count": req_data.get("cluster_size"),
                  "max_count": req_data.get("cluster_size"),
                  "flavorRef": flavor_id,
                  "networks": [{"uuid": net_id}],
                  "return_reservation_id": True,
                  "key_name": req_data.get("key-name")
                 }
        # Set the instance's volume by using image
        block_device_mapping_v2 = []
        bd = {
              "destination_type": "volume",
              "boot_index": 0,
              "source_type": "image",
              "uuid": image_id,
              "delete_on_termination": True,
              "volume_size": req_data.get("node-disk-size")
             }
        block_device_mapping_v2.append(bd)
        server["block_device_mapping_v2"] = block_device_mapping_v2
        request_data = {"server": server}
        resp_data = await Instance(svc_token_pack).post(request_data)
        if await self._check_resp_data(resp_data, 202, res_id,
                f"Create Monitor Cluster Server {res_id} failed!"):
            return
        # Config the cluster instances for instance_ids and ports
        task = asyncio.create_task(self.task_config_cluster_server(
            res_id, req_data, resp_data.get("data").get("reservation_id")))
        task.add_done_callback(util.task_done_cb)
        log.info("Request of Creating cluster Server has been sent.")

    async def task_delete_cluster(self, cluster):
        svc_token_pack = await Auth().get_svc_token(zone_conf)
        # Delete the port of virtual ip
        for vip_id in ["internal_id", "external_id"]:
            vip_id = cluster.get(vip_id)
            if vip_id:
                resp_data = await Port(svc_token_pack).delete(vip_id)
                if await self._check_resp_data(resp_data, 204,
                        cluster.get("id"),
                        f"Delete virtual IP {vip_id} failed!"):
                    if resp_data.get("status") != 404:
                        return
        # Delete the attached interfaces
        query = {"cluster_id": cluster.get("id")}
        interfaces = await db.get("cluster_interface", query)
        virtual_port_id = None
        if len(interfaces) > 0:
            virtual_port_id = interfaces[0].get("virtual_port_id")
            for interface in interfaces:
                await Port(svc_token_pack).delete(interface.get("id"))
                await db.delete("cluster_interface", interface.get("id"))
        # Delete the cluster of servers and port of subnet
        query = {"cluster_id": cluster.get("id")}
        server_ids = await db.get("cluster_instance", query)
        for server in server_ids:
            server_id = server.get("id")
            resp_data = await Instance(svc_token_pack).delete(server_id)
            if await self._check_resp_data(resp_data, 204, cluster.get("id"),
                    f"Delete server {server_id} failed!"):
                if resp_data.get("status") != 404:
                    return
            if len(server_ids) != 1:
                await Port(svc_token_pack).delete(server.get("port_id"))
                if virtual_port_id:
                    await Port(svc_token_pack).delete(virtual_port_id)
        # Delete cluster from DB
        update = {"deleted": True, "status": "deleted"}
        await db.update(self.table_name, cluster.get("id"), update)

    @staticmethod
    def _general_random_password():
        letters = string.ascii_letters
        digits = string.digits
        alphabet = letters + digits
        pwd_length = 8
        while True:
            pwd = ''
            for i in range(pwd_length):
                pwd += ''.join(secrets.choice(alphabet))

            if sum(char in digits for char in pwd) >= 2:
                break
        return pwd

    def _validate_request(self, req):
        if req.get("name") is None:
            log.error(f"cluster name in request cannot be None.")
            return {"status": 400, "data": {
                "message": f"cluster name in request cannot be None."}}
        if len(req.get("name")) > 128:
            log.error(f"cluster name in request is too long.")
            return {"status": 400, "data": {
                "message": f"cluster name in request is too long."}}
        if req.get("subnet_id") is None:
            log.error(f"subnet id in request cannot be None.")
            return {"status": 400, "data": {
                "message": f"subnet id in request cannot be None."}}
        cluster_size = req.get("cluster_size")
        if cluster_size and (cluster_size > 5 or cluster_size < 1):
            log.error(f"cluster_size is invalid value.")
            return {"status": 400, "data": {
                "message": f"cluster_size should be 1 <= value <= 5."}}
        if req.get("monitor_username") is None:
            req["monitor_username"] = "monitor_user"
        if req.get("monitor_password") is None:
            req["monitor_password"] = self._general_random_password()

    async def rh_post(self, c_req_data):
        log.info("Create monitor cluster begin.")
        req = c_req_data.get(self.res_name)
        error_message = self._validate_request(req)
        if error_message:
            return error_message
        # Get spec/image/disk_size/svc_mgmt/security_group from config file.
        if not self._get_config_values(req):
            return {"status": 400, "data": {
                "message": f"Missing value in conf file."}}
        # Create DB object and start the creation task
        cluster = {
                   "name": req.get("name"),
                   "cluster_size": req.get("cluster_size"),
                   "project_id": self.project_id,
                   "status": "building",
                   "security_group": req.get("node-sg")
                  }
        await db.add(self.table_name, cluster)
        task = asyncio.create_task(self.task_create_cluster_server(
            req, cluster.get("id")))
        task.add_done_callback(util.task_done_cb)
        log.info("Create monitor cluster is done.")
        return {"status": 202,
                "data": {self.res_name: {
                    "id": cluster.get("id"),
                    "password": req.get("monitor_password"),
                    "username": req.get("monitor_username")}}}

    async def rh_put(self, cluster_id, c_req_data):
        log.info("Update monitor cluster begin.")
        req = c_req_data.get(self.res_name)
        if req.get("name"):
            update = {"name": req.get("name")}
            await db.update(self.table_name, cluster_id, update)
        return {"status": 202, "data": {self.res_name: {"id": cluster_id}}}

    async def rh_delete(self, cluster_id=None, force=False):
        log.info("Delete monitor cluster begin.")
        cluster = await self.get_obj(cluster_id)
        if not cluster:
            return {"status": 404, "data": {
                    "message": f"Can't find the cluster."}}
        if not force and cluster.get("status") not in\
                ["error", "deleting", "active"]:
            log.error(f"Can't delete cluster with {cluster.get('status')}!")
            return {"status": 400, "data": {
                    "message": f"Can't delete cluster with current status."}}
        update = {"status": "deleting"}
        await db.update(self.table_name, cluster_id, update)
        # Delete dashboard configures from monitor ui.
        query = {"cluster_id": cluster.get("id")}
        server_ids = await db.get("cluster_instance", query)
        if not server_ids:
            update = {"deleted": True, "status": "deleted"}
            await db.update(self.table_name, cluster.get("id"), update)
            return {"status": 204,
                    "data": {self.res_name: {"id": cluster_id}}}
        mf_path = f"{self.cluster_path}/{cluster_id}/manifest"
        cluster_host = server_ids[0].get("fixed_address")
        if config['monitor']["monitor-ui"] == "None":
            monitor_ui_host = cluster_host
        else:
            monitor_ui_host = config['monitor']["monitor-ui"]
        cmd = f"{mf_path}/config-monitor-portal delete {monitor_ui_host}"
        with open(self.config_log, "a") as fd:
            rc = await util.exec_cmd(cmd, output_file=fd)
        if rc:
            log.error(f"Delete monitor dashboard failed!")
        else:
            log.info(f"Delete monitor portal done!")
        # Delete the ips and instances
        task = asyncio.create_task(self.task_delete_cluster(cluster))
        task.add_done_callback(util.task_done_cb)
        # Clear the cluster's scripts
        mf_path = f"{self.cluster_path}/{cluster_id}"
        cmd = f"rm -rf {mf_path}"
        await util.exec_cmd(cmd)
        return {"status": 202}

    async def task_config_monitor_portal(self, cluster_id, data):
        log.info(f"Config the monitor portal.")
        mf_path = f"{self.cluster_path}/{cluster_id}/manifest"
        os.makedirs(mf_path, exist_ok=True)
        t = self.j2_env.get_template(f"config-monitor-portal.j2")
        with open(f"{mf_path}/config-monitor-portal", "w") as fd:
            fd.write(t.render(data))
        cmd = f"chmod +x {mf_path}/config-monitor-portal"
        await util.exec_cmd(cmd)
        for dashboard in ["monitor", "kubernetes"]:
            cmd = f"cp {self.serv_path}/monitor-template/{dashboard}.json" \
                f" {mf_path}/"
            await util.exec_cmd(cmd)
        cmd = f"cp {self.serv_path}/monitor-template/update_dashboard.py" \
                f" {mf_path}/"
        await util.exec_cmd(cmd)
        internal_address = data.get("internal_address")
        if config['monitor']["monitor-ui"] == "None":
            monitor_ui_host = internal_address
        else:
            monitor_ui_host = config['monitor']["monitor-ui"]
        cmd = f"{mf_path}/config-monitor-portal config {monitor_ui_host}" \
              f" {internal_address} {mf_path}"
        with open(self.config_log, "a") as fd:
            rc = await util.exec_cmd(cmd, output_file=fd)
        if rc:
            log.error(f"Config monitor portal failed!")
            update = {"status": "error"}
            await db.update(self.table_name, cluster_id, update)
        else:
            log.info(f"Config monitor portal done!")
            update = {"status": "active"}
            await db.update(self.table_name, cluster_id, update)

    async def task_config_cluster_ha(self, cluster_id, data):
        log.info(f"Config the cluster ha.")
        internal_address = data.get("internal_address")
        external_address = data.get("external_address")
        cluster_hosts = data.get("cluster_hosts")
        cluster_ips = []
        for host_ip in cluster_hosts:
            cluster_ips.append(host_ip.get("port_ip"))
        cluster_ips = " ".join(cluster_ips)
        mf_path = f"{self.cluster_path}/{cluster_id}/manifest"
        cmd = f"{mf_path}/config-monitor-portal servers '{cluster_ips}'" \
              f" {external_address} {internal_address}"
        with open(self.config_log, "a") as fd:
            rc = await util.exec_cmd(cmd, output_file=fd)
        if rc:
            log.error(f"Config cluster ha failed!")
            update = {"status": "error"}
            await db.update(self.table_name, cluster_id, update)
        else:
            log.info(f"Config cluster ha done!")
            update = {"status": "active"}
            await db.update(self.table_name, cluster_id, update)

    async def task_update_cluster_ha(self, cluster_id, data, delete=False):
        log.info(f"Update the cluster ha.")
        virtual_address = data.get("virtual_address")
        interface_addresses = data.get("interface_addresses")
        cluster_ips = data.get("cluster_ips")
        mf_path = f"{self.cluster_path}/{cluster_id}/manifest"
        cmd = f"{mf_path}/config-monitor-portal update '{cluster_ips}'" \
              f" {virtual_address} '{interface_addresses}' {delete}"
        with open(self.config_log, "a") as fd:
            rc = await util.exec_cmd(cmd, output_file=fd)
        if rc:
            log.error(f"Update cluster ha failed!")
        else:
            log.info(f"Update cluster ha done!")

    async def task_create_jwt_token(self, c_req_data):
        log.info(f"Create the grafana jwt auth token.")
        req = c_req_data.get("auth")
        # Load JWKSet from file
        f"{self.serv_path}/monitor-template"
        with open(f"{self.serv_path}/monitor-template/jwks.json", 'r') as f:
            jwks = json.load(f)
        # Create a JWK object from the JSON data
        private_key = jwk.JWK.from_json(json.dumps(jwks['keys'][0]))
        # Prepare claims
        now_time = datetime.now()
        exp_hours = req.get("expired_time")
        claims = {
            "sub": req.get("user_name"),
            "nbf": int(now_time.timestamp()),
            "role": "Editor",
            "exp": int((now_time + timedelta(hours=exp_hours)).timestamp()),
            "iat": int(now_time.timestamp())}
        # Create and sign JWT
        token = jwt.JWT(header={"kid": private_key.key_id,
                "typ": "JWT", "alg": "RS256"}, claims=claims)
        token.make_signed_token(private_key)
        return {"status": 202, "data": {'auth': {"token": token.serialize()}}}

    async def task_attach_interface(self, cluster, c_req_data):
        log.info(f"Attach interface to monitor cluster.")
        req = c_req_data.get("interface")
        if not self._get_config_values(req):
            return {"status": 400, "data": {
                "message": f"Missing value in conf file."}}
        subnet_id = req.get("subnet_id")
        resp_data = await Subnet(self.token_pack).get(subnet_id)
        if resp_data.get("status") == 404:
            return {"status": 400, "data": {
                "message": f"Can not find the subnet."}}
        req["cluster_size"] = cluster.get("cluster_size")
        # Create ports for cluster servers
        ports = []
        result = await self._batch_create_subnet_port(cluster.get("id"),
                req, ports)
        if not result:
            return {"status": 500, "data": {
                    "message": f"Create interface failed."}}
        # Create virtual ip port for user subnet ports
        vip_address = await self._associate_vip(cluster.get("id"), req,
                req.get("user_network_id"), req.get("subnet_id"),
                req.get("node-sg"), ports)
        if not vip_address:
            return {"status": 500, "data": {
                    "message": f"Create VIP for interface failed."}}
        # Attach port to servers
        query = {"cluster_id": cluster.get("id")}
        instances = await db.get("cluster_instance", query)
        svc_token_pack = await Auth().get_svc_token(zone_conf)
        cluster_ips = []
        interface_addresses = []
        for port in ports:
            instance = instances.pop()
            instance_id = instance.get("id")
            cluster_ips.append(instance.get("fixed_address"))
            interface = {"port_id": port.get("port_id")}
            request_data = {"interfaceAttachment": interface}
            resp_data = await Instance(svc_token_pack).add_interface(
                instance_id, request_data)
            if await self._check_resp_data(resp_data, 200, cluster.get("id"),
                    f"Attach port to server {instance_id} failed!"):
                return {"status": 500, "data": {
                        "message": f"Attach interface failed."}}
            interface = {"virtual_address": vip_address.get("port_ip"),
                    "virtual_port_id": vip_address.get("port_id"),
                    "interface_address": port.get("port_ip"),
                    "instance_id": instance_id,
                    "cluster_id": cluster.get("id"),
                    "id": port.get("port_id")}
            await db.add("cluster_interface", interface)
            interface_addresses.append(port.get("port_ip"))
        if cluster.get("cluster_size") > 1:
            data = {"virtual_address": vip_address.get("port_ip"),
                    "cluster_ips": " ".join(cluster_ips),
                    "interface_addresses": " ".join(interface_addresses)}
            await self.task_update_cluster_ha(cluster.get("id"), data)
        data = {'interface': {
                "virtual_address": vip_address.get("port_ip"),
                "virtual_port_id": vip_address.get("port_id")}}
        return {"status": 200, "data": data}

    async def task_detach_interface(self, cluster, interface_id):
        query = {"virtual_port_id": interface_id}
        interfaces = await db.get("cluster_interface", query)
        svc_token_pack = await Auth().get_svc_token(zone_conf)
        # Update keepalived config first
        if cluster.get("cluster_size") > 1:
            query = {"cluster_id": cluster.get("id")}
            instances = await db.get("cluster_instance", query)
            cluster_ips = []
            interface_addresses = []
            for instances in instances:
                cluster_ips.append(instances.get("fixed_address"))
            for interface in interfaces:
                interface_addresses.append(interface.get("interface_address"))
            data = {"virtual_address": interfaces[0].get("virtual_address"),
                    "cluster_ips": " ".join(cluster_ips),
                    "interface_addresses": " ".join(interface_addresses)}
            await self.task_update_cluster_ha(cluster.get("id"), data, True)
        # Detach ports from cluster servers
        for interface in interfaces:
            instance_id = interface.get("instance_id")
            port_id = interface.get("id")
            resp_data = await Instance(svc_token_pack).remove_interface(
                instance_id, port_id)
            if await self._check_resp_data(resp_data, 202, cluster.get("id"),
                    f"Detach port from server {instance_id} failed!"):
                return {"status": 500, "data": {
                        "message": f"Detach interface failed."}}
            # Delete interface ports
            await Port(svc_token_pack).delete(port_id)
            await db.delete("cluster_interface", port_id)
        # Delete virtual ports
        await Port(svc_token_pack).delete(interface_id)
        return {"status": 204}

    async def rh_post_action(self, cluster_id, c_req_data):
        log.info(f"Execute monitor service action.")
        cluster = await self.get_obj(cluster_id)
        if not cluster:
            return {"status": 404, "data": {
                    "message": f"Can't find the cluster."}}
        if cluster.get("status") != "active":
            log.error(f"Can't action with {cluster.get('status')}!")
            return {"status": 400, "data": {
                    "message": f"Can't action with current status."}}
        if c_req_data.get("auth") is not None:
            return await self.task_create_jwt_token(c_req_data)
        elif c_req_data.get("interface") is not None:
            return await self.task_attach_interface(cluster, c_req_data)
        else:
            return {"status": 400}

    async def rh_delete_interface(self, cluster_id=None, interface_id=None):
        log.info(f"Detach interface from monitor cluster.")
        cluster = await self.get_obj(cluster_id)
        return await self.task_detach_interface(cluster, interface_id)

    async def rh_get(self, id):
        obj = await self.get_obj(id)
        if obj:
            obj["interfaces"] = await db.get("cluster_interface",
                    {"cluster_id": id})
            return {"status": 200, "data": {self.res_name: obj}}
        else:
            return {"status": 404}

