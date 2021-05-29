from typing import Optional

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

from db import database
from dbmodels import Admin, Client


def client_auth(
        bearer: HTTPAuthorizationCredentials = Depends(HTTPBearer(scheme_name="Client Token")),
        db: Session = Depends(database)) -> Client:

    client: Optional[Client] = db.query(Client).filter(Client.token == bearer.credentials).one_or_none()

    if client is not None:
        return client

    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="Invalid authentication credentials"
    )


def admin_auth(
        creds: HTTPBasicCredentials = Depends(HTTPBasic(scheme_name="Admin Token")),
        db: Session = Depends(database)) -> Admin:

    admin: Optional[Admin] = db.query(Admin).filter(Admin.username == creds.username).one_or_none()

    if admin is not None:
        return admin

    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="Invalid authentication credentials"
    )
