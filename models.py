from typing import Optional, Dict, List
from typing_extensions import Annotated

from pydantic import BaseModel, Field


class Admin(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class CpuCacheInfo(BaseModel):
    l1d: Annotated[int, Field(title="Level 1 Data Cache (bytes)")]
    l1i: Annotated[int, Field(title="Level 1 Instruction Cache (bytes)")]
    l2: Annotated[int, Field(title="Level 2 Cache (megibytes)")]
    l3: Annotated[Optional[int], Field(title="Level 3 Cache (megibytes)")]

    class Config:
        title = "CPU Cache Information"
        orm_mode = True


class CpuInfo(BaseModel):
    manufacturer: str
    brand: str
    vendor: str
    family: str
    model: Optional[str]
    stepping: Optional[str]
    revision: Optional[str]
    voltage: Optional[str]
    speed: Annotated[float, Field(title="Clock Frequency in GHz")]
    speedMin: Annotated[Optional[float], Field(title="Minimum Clock Frequency in GHz")]
    speedMax: Annotated[float, Field(title="Maximum Clock Frequency in GHz")]
    governor: Optional[str]
    cores: int
    physicalCores: int
    efficiencyCores: Optional[int]
    "LITTLE-cores when a big.LITTLE configuration is used."
    performanceCores: Optional[int]
    "big-cores when a big.LITTLE configuration is used."
    processors: int
    socket: Optional[str]
    flags: str
    virtualization: Annotated[bool, Field(title="Whether virtualization is supported")]
    cache: CpuCacheInfo

    class Config:
        title = "CPU Information"
        orm_mode = True


class OsInfo(BaseModel):
    platform: str
    distro: str
    release: str
    codename: Optional[str]
    kernel: str
    arch: str
    codepage: str
    logofile: str
    build: str
    servicepack: Optional[str]
    uefi: bool
    hypervisor: Optional[bool]
    remoteSession: Optional[bool]

    class Config:
        title = "Operating System Information"
        orm_mode = True


class RaspberryInfo(BaseModel):
    manufacturer: str
    processor: str
    type: str
    revision: str

    class Config:
        title = "Raspberry Pi Information"
        orm_mode = True


class SystemInfo(BaseModel):
    manufacturer: Optional[str]
    model: Optional[str]
    version: Optional[str]
    sku: Optional[str]
    virtual: bool
    virtualHost: Optional[str]
    raspberry: Optional[RaspberryInfo]

    class Config:
        title = "System Information"
        orm_mode = True


class DockerInfo(BaseModel):
    kernelVersion: str
    operatingSystem: str
    osVersion: str
    osType: str
    architecture: str
    ncpu: int
    memTotal: int
    serverVersion: str

    class Config:
        orm_mode = True


class ClientMeta(BaseModel):
    cpu: CpuInfo
    os: OsInfo
    system: SystemInfo
    docker: DockerInfo

    class Config:
        title = "Client Properties"


class Result(BaseModel):
    implementation: str
    solution: str
    label: str
    passes: int
    duration: float
    threads: int
    tags: Dict[str, str]
    client_id: Optional[int]
    "The client MUST NOT submit this value, it will be ignored."

    class Config:
        orm_mode = True
        title = "Result"


class Client(BaseModel):
    id: int
    token: str

    owner: Admin

    results: List[Result]

    cpu: Optional[CpuInfo]
    os: Optional[OsInfo]
    system: Optional[SystemInfo]
    docker: Optional[DockerInfo]

    class Config:
        orm_mode = True
        title = "Client"
