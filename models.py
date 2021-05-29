from typing import Optional

from pydantic import BaseModel


class Admin(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class ClientMeta(BaseModel):
    os: str
    arch: str
    cpuname: str

    class Config:
        title = "Client System Properties"


class Client(BaseModel):
    id: int
    token: str

    os: Optional[str]
    arch: Optional[str]
    cpuname: Optional[str]

    owner: Admin

    class Config:
        orm_mode = True
        title = "Client"
