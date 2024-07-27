import os
import logging
import requests
import config as c
from exceptions import DownloadError

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARN').upper()
logging.basicConfig(level=LOGLEVEL)
logger = (logging.getLogger(__name__),)


def get_data(queue_id: str, annotation_id: str):
    logging.debug("Downloading data for: %s %s", queue_id, annotation_id)

    # Download data from Rossum API
    rossum_response = requests.get(
        # TODO discuss trailing slash in APP_URL
        f"{c.APP_URL}queues/{queue_id}/export?format=xml&id={annotation_id}",
        headers={"Authorization": f"Bearer {c.ROSSUM_API_KEY}"},
    )

    logging.debug("We got this response code: %s", rossum_response.status_code)
    logging.debug("We got this data: %s", rossum_response.text)

    if rossum_response.status_code != 200:
        raise DownloadError(rossum_response.status_code)
    # we can do more validations like if it is a real xml, containing something etc.

    return rossum_response.text.encode()  # Would you work with byte string or string?
