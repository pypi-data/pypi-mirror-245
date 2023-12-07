"""
The objects of monitor service.
"""
from pydantic import BaseModel


class MonitorClusterObject(BaseModel):
    name: str
    subnet_id: str
    service_address: str = None
    cluster_size: int = 1
    monitor_username: str = None
    monitor_password: str = None


class MonitorClusterPost(BaseModel):
    cluster: MonitorClusterObject


class MonitorClusterPutObject(BaseModel):
    name: str = None


class MonitorClusterPut(BaseModel):
    cluster: MonitorClusterPutObject


class MonitorClusterAuthObject(BaseModel):
    user_name: str
    expired_time: int = 1


class MonitorClusterAction(BaseModel):
    auth: MonitorClusterAuthObject


class MonitorClusterInterfaceObject(BaseModel):
    subnet_id: str


class MonitorClusterInterface(BaseModel):
    interface: MonitorClusterInterfaceObject

