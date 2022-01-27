import httpx
import os

from fastapi import Depends, FastAPI, Header, HTTPException, status
from typing import Optional
from fastapi.security import HTTPBasicCredentials, HTTPBearer

security = HTTPBearer()

ACCESS_SERVICE_URL = os.getenv('ACCESS_SERVICE_URL')

app = FastAPI(openapi_url="/api/a/openapi.json", docs_url="/api/a/docs")


def has_access(credentials: HTTPBasicCredentials = Depends(security)):
    response = httpx.get(os.getenv('ACCESS_SERVICE_URL'), headers={'Authorization': credentials.credentials})
    if response.status_code == 401:
        raise HTTPException(status_code=401)


@app.get('/api/a/unprotected_a')
async def unprotected_a():
    return {"Protected": False}


@app.get('/api/a/protected_a', dependencies=[Depends(has_access)])
async def protected_a():
    return {"Protected": True}


@app.get('/api/a/protected_b', dependencies=[Depends(has_access)])
async def protected_b():
    return {"Protected": True}
