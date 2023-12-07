import logging

import compute
import network
from client.common import ResourceBase
from client.common import get_svc_url

log = logging.getLogger("cms")


class NFS(ResourceBase):
    def __init__(self, args, token_pack):
        super().__init__(args, token_pack)
        self.type = "cluster"
        svc_url = get_svc_url(token_pack, "cms-builder")
        self.url = f"{svc_url}/nfs"

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

    def list_directory(self):
        id = self.get_id_by_name(self.args.name)
        if not id:
            return
        url = f"{self.url}/{id}/directory"
        resp = self.send_req("get", url, self.headers)
        print(f"RC: {resp.status_code}")
        print(f"Response: {resp.text}")

    def add_directory(self):
        id = self.get_id_by_name(self.args.name)
        if not id:
            return
        url = f"{self.url}/{id}/directory"
        data = {"directory": {
                "name": self.args.directory_name,
                "size": self.args.size}}
        resp = self.send_req("post", url, self.headers, data)
        print(f"RC: {resp.status_code}")
        print(f"Response: {resp.text}")

    def remove_directory(self):
        id = self.get_id_by_name(self.args.name)
        if not id:
            return
        url = f"{self.url}/{id}/directory/{self.args.directory_name}"
        resp = self.send_req("delete", url, self.headers)
        print(f"RC: {resp.status_code}")
        print(f"Response: {resp.text}")


arg_schema = {
    "nfs": {
        "res-class": NFS,
        "list": [],
        "list-instance": [
            {"name": "name"}
        ],
        "show": [
            {"name": "name"}
        ],
        "create": [
            {"name": "name"},
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
        ],
        "list-directory": [
            {"name": "name"}
        ],
        "add-directory": [
            {"name": "name"},
            {
                "name": "--size",
                "attr": {
                    "required": True
                }
            },
            {
                "name": "--directory-name",
                "attr": {
                    "required": True
                }
            }
        ],
        "remove-directory": [
            {"name": "name"},
            {
                "name": "--directory-name",
                "attr": {
                    "required": True
                }
            }
        ]
    }
}

