import logging

import compute
import network
from client.common import ResourceBase
from client.common import get_svc_url

log = logging.getLogger("cms")


class MariaDB(ResourceBase):
    def __init__(self, args, token_pack):
        super().__init__(args, token_pack)
        self.type = "cluster"
        svc_url = get_svc_url(token_pack, "cms-builder")
        self.url = f"{svc_url}/mariadb"

    def create(self):
        spec_id = compute.Spec(self.args, self.token_pack).get_id_by_name(
                self.args.spec)
        if not spec_id:
            return
        subnet_id = network.Subnet(self.args, self.token_pack).get_id_by_name(
                self.args.subnet)
        if not subnet_id:
            return
        res = {"name": self.args.name,
                "cluster_size": self.args.cluster_size,
                "subnet_id": subnet_id,
                "spec_id": spec_id}
        if self.args.volume_size:
            res["volume_size"] = self.args.volume_size
        data = {self.type: res}
        resp = self.send_req("post", self.url, self.headers, data)
        print(f"RC: {resp.status_code}")
        print(f"Response: {resp.text}")

    def set(self):
        id = self.get_id_by_name(self.args.name)
        if not id:
            return
        res = {}
        if self.args.status:
            res["status"] = self.args.status
        data = {self.type: res}
        url = f"{self.url}/{id}"
        resp = self.send_req("put", url, self.headers, data)
        print(f"RC: {resp.status_code}")
        print(f"Response: {resp.text}")


class PostgreSQL(ResourceBase):
    def __init__(self, args, token_pack):
        super().__init__(args, token_pack)
        self.type = "cluster"
        svc_url = get_svc_url(token_pack, "cms-builder")
        self.url = f"{svc_url}/postgresql"

    def create(self):
        spec_id = compute.Spec(self.args, self.token_pack).get_id_by_name(
                self.args.spec)
        if not spec_id:
            return
        subnet_id = network.Subnet(self.args, self.token_pack).get_id_by_name(
                self.args.subnet)
        if not subnet_id:
            return
        res = {"name": self.args.name,
                "cluster_size": self.args.cluster_size,
                "subnet_id": subnet_id,
                "spec_id": spec_id}
        if self.args.volume_size:
            res["volume_size"] = self.args.volume_size
        data = {self.type: res}
        resp = self.send_req("post", self.url, self.headers, data)
        print(f"RC: {resp.status_code}")
        print(f"Response: {resp.text}")

    def set(self):
        id = self.get_id_by_name(self.args.name)
        if not id:
            return
        res = {}
        if self.args.status:
            res["status"] = self.args.status
        data = {self.type: res}
        url = f"{self.url}/{id}"
        resp = self.send_req("put", url, self.headers, data)
        print(f"RC: {resp.status_code}")
        print(f"Response: {resp.text}")


class Redis(ResourceBase):
    def __init__(self, args, token_pack):
        super().__init__(args, token_pack)
        self.type = "cluster"
        svc_url = get_svc_url(token_pack, "cms-builder")
        self.url = f"{svc_url}/redis"

    def create(self):
        spec_id = compute.Spec(self.args, self.token_pack).get_id_by_name(
                self.args.spec)
        if not spec_id:
            return
        subnet_id = network.Subnet(self.args, self.token_pack).get_id_by_name(
                self.args.subnet)
        if not subnet_id:
            return
        res = {"name": self.args.name,
                "cluster_size": self.args.cluster_size,
                "subnet_id": subnet_id,
                "spec_id": spec_id}
        if self.args.volume_size:
            res["volume_size"] = self.args.volume_size
        data = {self.type: res}
        resp = self.send_req("post", self.url, self.headers, data)
        print(f"RC: {resp.status_code}")
        print(f"Response: {resp.text}")

    def set(self):
        id = self.get_id_by_name(self.args.name)
        if not id:
            return
        res = {}
        if self.args.status:
            res["status"] = self.args.status
        data = {self.type: res}
        url = f"{self.url}/{id}"
        resp = self.send_req("put", url, self.headers, data)
        print(f"RC: {resp.status_code}")
        print(f"Response: {resp.text}")


class RabbitMQ(ResourceBase):
    def __init__(self, args, token_pack):
        super().__init__(args, token_pack)
        self.type = "cluster"
        svc_url = get_svc_url(token_pack, "cms-builder")
        self.url = f"{svc_url}/rabbitmq"

    def create(self):
        spec_id = compute.Spec(self.args, self.token_pack).get_id_by_name(
                self.args.spec)
        if not spec_id:
            return
        subnet_id = network.Subnet(self.args, self.token_pack).get_id_by_name(
                self.args.subnet)
        if not subnet_id:
            return
        res = {"name": self.args.name,
                "cluster_size": self.args.cluster_size,
                "subnet_id": subnet_id,
                "spec_id": spec_id}
        data = {self.type: res}
        resp = self.send_req("post", self.url, self.headers, data)
        print(f"RC: {resp.status_code}")
        print(f"Response: {resp.text}")

    def set(self):
        id = self.get_id_by_name(self.args.name)
        if not id:
            return
        res = {}
        if self.args.status:
            res["status"] = self.args.status
        data = {self.type: res}
        url = f"{self.url}/{id}"
        resp = self.send_req("put", url, self.headers, data)
        print(f"RC: {resp.status_code}")
        print(f"Response: {resp.text}")


arg_schema = {
    "mariadb": {
        "res-class": MariaDB,
        "list": [],
        "list-instance": [
            {"name": "name"}
        ],
        "show": [
            {"name": "name"}
        ],
        "create": [
            {"name": "name"},
            {"name": "--volume-size"},
            {
                "name": "--cluster-size",
                "attr": {
                    "default": 1
                }
            },
            {
                "name": "--subnet",
                "attr": {
                    "required": True
                }
            },
            {
                "name": "--spec",
                "attr": {
                    "required": True
                }
            }
        ],
        "set": [
            {"name": "name"},
            {"name": "--status"}
        ],
        "delete": [
            {"name": "name"}
        ]
    },
    "postgresql": {
        "res-class": PostgreSQL,
        "list": [],
        "list-instance": [
            {"name": "name"}
        ],
        "show": [
            {"name": "name"}
        ],
        "create": [
            {"name": "name"},
            {"name": "--volume-size"},
            {
                "name": "--cluster-size",
                "attr": {
                    "default": 1
                }
            },
            {
                "name": "--subnet",
                "attr": {
                    "required": True
                }
            },
            {
                "name": "--spec",
                "attr": {
                    "required": True
                }
            }
        ],
        "set": [
            {"name": "name"},
            {"name": "--status"}
        ],
        "delete": [
            {"name": "name"}
        ]
    },
    "redis": {
        "res-class": Redis,
        "list": [],
        "list-instance": [
            {"name": "name"}
        ],
        "show": [
            {"name": "name"}
        ],
        "create": [
            {"name": "name"},
            {"name": "--volume-size"},
            {
                "name": "--cluster-size",
                "attr": {
                    "default": 1
                }
            },
            {
                "name": "--subnet",
                "attr": {
                    "required": True
                }
            },
            {
                "name": "--spec",
                "attr": {
                    "required": True
                }
            }
        ],
        "set": [
            {"name": "name"},
            {"name": "--status"}
        ],
        "delete": [
            {"name": "name"}
        ]
    },
    "rabbitmq": {
        "res-class": RabbitMQ,
        "list": [],
        "list-instance": [
            {"name": "name"}
        ],
        "show": [
            {"name": "name"}
        ],
        "create": [
            {"name": "name"},
            {"name": "--volume-size"},
            {
                "name": "--cluster-size",
                "attr": {
                    "default": 1
                }
            },
            {
                "name": "--subnet",
                "attr": {
                    "required": True
                }
            },
            {
                "name": "--spec",
                "attr": {
                    "required": True
                }
            }
        ],
        "set": [
            {"name": "name"},
            {"name": "--status"}
        ],
        "delete": [
            {"name": "name"}
        ]
    }
}

