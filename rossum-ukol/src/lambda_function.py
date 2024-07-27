import os
import secrets
import hashlib
import logging

from typing import Annotated

from mangum import Mangum
from fastapi import Depends, FastAPI, HTTPException, status, Path, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse

import config as c
from data_downloader import get_data
from transform import transform
from data_upload import upload_data

app = FastAPI()

security = HTTPBasic()

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARN').upper()
logging.basicConfig(level=LOGLEVEL)
logger = (logging.getLogger(__name__),)


def check_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    # one way to do it
    is_correct_username = secrets.compare_digest(credentials.username.encode(), c.USERNAME.encode())

    # better way to do it
    is_correct_password = hashlib.sha256(credentials.password.encode()).hexdigest() == c.PASSWORD

    logging.debug("Username: %s", credentials.username)

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/healthcheck")
async def healtcheck():
    return {"message": "I live."}


# I assume id is/can be str and not just a number
@app.get("/export/{queue_id}/{annotation_id}")
async def export(
    queue_id: Annotated[str, Path(max_length=32)],
    annotation_id: Annotated[str, Path(max_length=32)],
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    check_credentials(credentials)
    logging.info("We got request for %s %s", queue_id, annotation_id)

    # TODO extra validation? I did not create any model or so as it is just a int/str id
    # It should not be empty and not longer then some reasonable length
    # If we say it numberic only we can do such validation

    data = get_data(queue_id, annotation_id)
    transformed_data = transform(data)
    upload_data(annotation_id, transformed_data)

    return {"success": True}


# catch all exceptions from FastAPI
@app.exception_handler(Exception)
async def handle_error(request: Request, exp: Exception):

    logging.error(
        "There was a kaboom for request %s and resulting exception %s", request.path_params, str(exp)
    )  # TODO there are nice ways to serialize exceptions (however stacktrace is in the log anyway)
    return JSONResponse(
        status_code=200,
        content={"success": False},
    )


handler = Mangum(app)  # lambda integration
