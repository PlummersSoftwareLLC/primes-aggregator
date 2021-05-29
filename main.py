import secrets
from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
from auth import admin_auth, client_auth
from db import engine, database
from dbmodels import Admin, Client, Base

Base.metadata.create_all(bind=engine)
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
    db.refresh(client)
    return models.Client.from_orm(client)


@app.delete("/runners/{runner_id}", summary="Remove a runner", tags=["Bookkeeping"], response_model=bool)
def unregister(
        runner_id: int,
        _admin: Admin = Depends(admin_auth),
        db: Session = Depends(database)):
    db.query(Client).filter(Client.id == runner_id).delete()
    db.commit()
    return True


@app.patch("/runners", summary="Initialize a runner", tags=["Bookkeeping"])
def initialize(props: models.ClientMeta, client: Client = Depends(client_auth)):
    """
    Initialize a runner, and report system properties.
    """

    return None


@app.post("/results", summary="Publish a new result", tags=["Results"])
def publish_result(client: Client = Depends(client_auth)):
    pass


@app.get("/results", summary="List all results", tags=["Results"])
def list_results():
    pass
