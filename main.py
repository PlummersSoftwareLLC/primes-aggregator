import secrets
from typing import List, Generator

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
from auth import admin_auth, client_auth
from db import database
from dbmodels import Admin, Client, Result, DockerInfo, RaspberryInfo, SystemInfo, OsInfo, CacheInfo, CpuInfo

app = FastAPI()

app.title = "Dragrace Results Aggregation Service"
app.version = "0.1"
app.description = """
This service manages benchmark runners and aggregates their results.
"""


@app.get("/runners", summary="List runners", tags=["Bookkeeping"], response_model=List[models.Client])
def list_clients(
        _admin: Admin = Depends(admin_auth),
        db: Session = Depends(database)) -> List[models.Client]:

    clients: List[Client] = db.query(Client).all()
    return [models.Client.from_orm(client) for client in clients]


@app.post("/runners", summary="Add a new runner", tags=["Bookkeeping"], response_model=models.Client)
def register(
        admin: Admin = Depends(admin_auth),
        db: Session = Depends(database)) -> models.Client:
    client = Client(owner=admin, token=secrets.token_hex(nbytes=64))
    db.add(client)
    db.commit()
    db.expire(client, ("id", ))
    return models.Client.from_orm(client)


@app.delete("/runners/{runner_id}", summary="Remove a runner", tags=["Bookkeeping"])
def unregister(
        runner_id: int,
        admin: Admin = Depends(admin_auth),
        db: Session = Depends(database)):
    db.autocommit = False

    client: Client = db.query(Client).filter(Client.id == runner_id).one_or_none()

    if client.system is not None:
        if client.system.raspberry is not None:
            db.delete(client.system.raspberry)
        db.delete(client.system)

    if client.docker is not None:
        db.delete(client.docker)

    if client.cpu is not None:
        if client.cpu.cache is not None:
            db.delete(client.cpu.cache)
        db.delete(client.cpu)

    if client.os is not None:
        db.delete(client.os)

    db.delete(client)

    db.commit()
    db.expire(admin, ("clients", ))


@app.patch("/runners", summary="Set current runner system info", tags=["Bookkeeping"])
def set_system_info(props: models.ClientMeta,
                    client: Client = Depends(client_auth),
                    db: Session = Depends(database)):
    """
    Initialize a runner, and report system properties.
    """

    if client.docker is not None:
        client.docker.__dict__.update(props.docker.__dict__)
    else:
        client.docker = DockerInfo(**props.docker.__dict__)

    db.add(client.docker)

    if client.system is not None:
        if props.system.raspberry is not None:
            if client.system.raspberry is not None:
                client.system.raspberry.__dict__.update(props.system.raspberry.__dict__)
            else:
                client.system.raspberry = RaspberryInfo(props.system.raspberry.__dict__)
        client.system.__dict__.update({k: v for k, v in props.system.__dict__.items() if k != "raspberry"})
    else:
        client.system = SystemInfo(**{k: v for k, v in props.system.__dict__.items() if k != "raspberry"})
        if props.system.raspberry is not None:
            client.system.raspberry = RaspberryInfo(props.system.raspberry.__dict__)

    if client.system.raspberry is not None:
        db.add(client.system.raspberry)
    db.add(client.system)

    if client.os is not None:
        client.os.__dict__.update(props.os.__dict__)
    else:
        client.os = OsInfo(**props.os.__dict__)

    db.add(client.os)

    if client.cpu is not None:
        if client.cpu.cache is not None:
            client.cpu.cache.__dict__.update(props.cpu.cache.__dict__)
        else:
            client.cpu.cache = CacheInfo(props.cpu.cache.__dict__)
        client.cpu.__dict__.update({k: v for k, v in props.cpu.__dict__.items() if k != "cache"})
    else:
        client.cpu = CpuInfo(**{k: v for k, v in props.cpu.__dict__.items() if k != "cache"})
        client.cpu.cache = CacheInfo(**props.cpu.cache.__dict__)

    db.add(client.cpu.cache)
    db.add(client.cpu)

    db.commit()


@app.post("/results", summary="Publish a new result", tags=["Results"])
def publish_result(
        result: models.Result,
        client: Client = Depends(client_auth),
        db: Session = Depends(database)):
    result = Result(
        **{
            **result.__dict__,
            "client_id": client.id,
        }
    )
    db.add(result)
    db.commit()
    db.expire(result, ("id", ))
    db.expire(client, ("results", ))


@app.get("/results", summary="List all results", tags=["Results"], response_model=List[models.Result])
def list_results(db: Session = Depends(database)):
    results: List[Result] = db.query(Result).all()
    return [models.Result.from_orm(result) for result in results]
