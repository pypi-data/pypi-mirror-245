import logging
import yaml

import compute
from client.common import ResourceBase
from client.common import get_svc_url

log = logging.getLogger("cms")


class Kubernetes(ResourceBase):
    def __init__(self, args, token_pack):
        super().__init__(args, token_pack)
        self.type = "cluster"
        if args.cms_api_url:
            self.url = f"{args.cms_api_url}/v1/kubernetes"
        else:
            svc_url = get_svc_url(token_pack, "cms-builder")
            self.url = f"{svc_url}/kubernetes"

    def create(self):
        params = {"name": self.args.name,
                "credential_name": self.args.cms_credential_name,
                "credential_secret": self.args.cms_credential_secret}
        map = {"control_size": self.args.control_size,
                "domain": self.args.domain,
                "api_access": self.args.api_access,
                "service_access": self.args.service_access,
                "api_address": self.args.api_address,
                "ingress_address": self.args.ingress_address,
                "pod_address_block": self.args.pod_address_block,
                "service_address_block": self.args.service_address_block,
                "node_subnet_address": self.args.node_subnet_address,
                "node_subnet_id": self.args.node_subnet,
                "corp_gateway_address": self.args.corp_gateway_address,
                "public_gateway_address": self.args.public_gateway_address,
                "internal_api_address": self.args.internal_api_address,
                "internal_ingress_address": self.args.internal_ingress_address,
                "security_group_id": self.args.security_group}
        for name in map.keys():
            if map[name]:
                params[name] = map[name]
        resp = self.send_req("post", self.url, self.headers,
                {"cluster": params})
        print(f"RC: {resp.status_code}")
        print(f"Response: {resp.text}")

    def set(self):
        id = self.get_id_by_name(self.args.name)
        if not id:
            return
        url = f"{self.url}/{id}"
        params = {"status": self.args.status}
        resp = self.send_req("put", url, self.headers, {"cluster": params})
        print(f"RC: {resp.status_code}")

    def add_worker(self):
        id = self.get_id_by_name(self.args.name)
        if not id:
            return
        spec_id = compute.Spec(self.args, self.token_pack).get_id_by_name(
                self.args.spec)
        if not spec_id:
            return
        url = f"{self.url}/{id}/worker"
        params = {"count": self.args.count,
                "spec_id": spec_id}
        resp = self.send_req("post", url, self.headers, {"worker": params})
        print(f"RC: {resp.status_code}")
        print(f"Response: {resp.text}")

    def get_config(self):
        id = self.get_id_by_name(self.args.name)
        if not id:
            return
        url = f"{self.url}/{id}/config"
        resp = self.send_req("get", url, self.headers)
        if resp.status_code == 200:
            print(yaml.dump(resp.json(), default_flow_style = False))
        else:
            print(f"RC: {resp.status_code}")

    def list_worker(self):
        id = self.get_id_by_name(self.args.name)
        if not id:
            return
        url = f"{self.url}/{id}/worker"
        resp = self.send_req("get", url, self.headers)
        print(f"RC: {resp.status_code}")
        print(f"Response: {resp.text}")


arg_schema = {
    "kubernetes": {
        "res-class": Kubernetes,
        "list": [],
        "show": [
            {"name": "name"}
        ],
        "create": [
            {"name": "name"},
            {"name": "--control-size"},
            {
                "name": "--api-access",
                "attr": {
                    "choices": ["corp", "public"]
                }
            },
            {
                "name": "--service-access",
                "attr": {
                    "choices": ["corp", "public"]
                }
            },
            {"name": "--domain"},
            {"name": "--api-address"},
            {"name": "--ingress-address"},
            {"name": "--pod-address-block"},
            {"name": "--service-address-block"},
            {"name": "--node-subnet-address"},
            {"name": "--node-subnet"},
            {"name": "--corp-gateway-address"},
            {"name": "--public-gateway-address"},
            {"name": "--internal-api-address"},
            {"name": "--internal-ingress-address"},
            {"name": "--security-group"}
        ],
        "set": [
            {"name": "name"},
            {"name": "--status"}
        ],
        "delete": [
            {"name": "name"}
        ],
        "add-worker": [
            {"name": "name"},
            {"name": "--count"},
            {"name": "--spec"}
        ],
        "get-config": [
            {"name": "name"}
        ],
        "list-worker": [
            {"name": "name"}
        ]
    }
}

