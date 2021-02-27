"""
Pydantic model of the response of getstatdetail
"""
from decimal import Decimal
from typing import List, Literal, Optional

from pydantic import AnyUrl, BaseModel, Field


class Connection(BaseModel):
    connected: bool
    switches: int
    uri: AnyUrl


class DeviceHardware(BaseModel):
    name: str
    pci: str
    sensors: List[Decimal]
    type: Literal["CPU", "GPU", "ACCELERATOR"]


class DeviceMining(BaseModel):
    hashrate: str
    pause_reason: Optional[str]
    paused: bool
    segment: List[str]
    shares: List[int]


class Device(BaseModel):
    index: int = Field(..., alias="_index")
    mode: Literal["OpenCL", "CUDA"] = Field(..., alias="_mode")
    hardware: DeviceHardware
    mining: DeviceMining


class Host(BaseModel):
    name: str
    runtime: int
    version: str


class Mining(BaseModel):
    difficulty: int
    epoch: int
    epoch_changes: int
    hashrate: str
    shares: List[int]


class Monitors(BaseModel):
    temperatures: List[int]


class GetStatDetail(BaseModel):
    connection: Connection
    devices: List[Device]
    host: Host
    mining: Mining
    monitors: Optional[Monitors]


class Result(BaseModel):
    result: GetStatDetail
