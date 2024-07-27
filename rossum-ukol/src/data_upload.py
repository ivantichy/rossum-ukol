import os
import base64
import logging
import requests
import config as c
from exceptions import UploadError

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARN').upper()
logging.basicConfig(level=LOGLEVEL)
logger = (logging.getLogger(__name__),)


def upload_data(annotation_id: str, payload: str):
    logging.debug("Uploading data for: %s", annotation_id)

    data = {"annotationId": annotation_id, "content": base64.b64encode(payload).decode()}

    upload_response = requests.post(f"{c.UPLOAD_URL}", json=data)
    logging.debug("We got this response code: %s", upload_response.status_code)
    logging.debug("We got this data: %s", upload_response.text)

    if upload_response.status_code != 200:  # or 201?
        raise UploadError(upload_response.status_code)
