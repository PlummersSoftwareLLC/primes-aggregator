import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey, PickleType, Float, Boolean
from sqlalchemy.orm import relationship

import hash
from db import Base


class Admin(Base):
    __tablename__ = "administrators"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String(128))

    clients = relationship("Client", back_populates="owner")

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        verify_result = hash.verify_password(self.password_hash, password)
        if isinstance(verify_result, bool):
            return verify_result

        self.password_hash = verify_result
        return True


class CacheInfo(Base):
    __tablename__ = "cache_info"
    id = Column(Integer, primary_key=True, index=True)

    l1d: Column(Integer)
    l1i: Column(Integer)
    l2: Column(Integer)
    l3: Column(Integer)

    cpu = relationship("CpuInfo", uselist=False, back_populates="cache")


class CpuInfo(Base):
    __tablename__ = "cpu_info"
    id = Column(Integer, primary_key=True, index=True)

    manufacturer = Column(String)
    brand = Column(String)
    vendor = Column(String)
    family = Column(String)
    model = Column(String)
    stepping = Column(String)
    revision = Column(String)
    voltage = Column(String)
    speed = Column(Float)
    speedMin = Column(Float)
    speedMax = Column(Float)
    governor = Column(String)
    cores = Column(Integer)
    physicalCores = Column(Integer)
    efficiencyCores = Column(Integer)
    performanceCores = Column(Integer)
    processors = Column(Integer)
    socket = Column(String)
    flags = Column(PickleType)
    virtualization = Column(Boolean)

    cache_id = Column(Integer, ForeignKey(CacheInfo.id), index=True)
    cache = relationship(CacheInfo, back_populates="cpu")

    client = relationship("Client", uselist=False, back_populates="cpu")


class OsInfo(Base):
    __tablename__ = "os_info"
    id = Column(Integer, primary_key=True, index=True)

    platform = Column(String)
    distro = Column(String)
    release = Column(String)
    codename = Column(String)
    kernel = Column(String)
    arch = Column(String)
    codepage = Column(String)
    logofile = Column(String)
    build = Column(String)
    servicepack = Column(String)
    uefi = Column(Boolean)
    hypervisor = Column(Boolean)
    remoteSession = Column(Boolean)

    client = relationship("Client", uselist=False, back_populates="os")


class RaspberryInfo(Base):
    __tablename__ = "raspberry_info"
    id = Column(Integer, primary_key=True, index=True)

    manufacturer = Column(String)
    processor = Column(String)
    type = Column(String)
    revision = Column(String)

    system = relationship("SystemInfo", uselist=False, back_populates="raspberry")


class SystemInfo(Base):
    __tablename__ = "system_info"
    id = Column(Integer, primary_key=True, index=True)

    manufacturer = Column(String)
    model = Column(String)
    version = Column(String)
    sku = Column(String)
    virtual = Column(Boolean)
    virtualHost = Column(String)

    raspberry_id = Column(Integer, ForeignKey(RaspberryInfo.id), index=True)
    raspberry = relationship(RaspberryInfo, back_populates="system")

    client = relationship("Client", uselist=False, back_populates="system")


class DockerInfo(Base):
    __tablename__ = "docker_info"
    id = Column(Integer, primary_key=True, index=True)

    kernelVersion = Column(String)
    operatingSystem = Column(String)
    osVersion = Column(String)
    osType = Column(String)
    architecture = Column(String)
    ncpu = Column(Integer)
    memTotal = Column(Integer)
    serverVersion = Column(String)

    client = relationship("Client", uselist=False, back_populates="docker")


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)

    results = relationship("Result", uselist=False, back_populates="client")

    owner_id = Column(Integer, ForeignKey(Admin.id), index=True)
    owner = relationship(Admin, back_populates="clients")

    system_id = Column(Integer, ForeignKey(SystemInfo.id), index=True)
    system = relationship(SystemInfo, back_populates="client")

    os_id = Column(Integer, ForeignKey(OsInfo.id), index=True)
    os = relationship(OsInfo, back_populates="client")

    cpu_id = Column(Integer, ForeignKey(CpuInfo.id), index=True)
    cpu = relationship(CpuInfo, back_populates="client")

    docker_id = Column(Integer, ForeignKey(DockerInfo.id), index=True)
    docker = relationship(DockerInfo, back_populates="client")


class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    implementation = Column(String)
    solution = Column(String)
    label = Column(String)
    passes = Column(Integer)
    duration = Column(Float)
    threads = Column(Integer)
    tags = Column(PickleType)

    client_id = Column(Integer, ForeignKey(Client.id), index=True)
    client = relationship(Client, back_populates="results")
