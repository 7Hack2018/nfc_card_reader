import requests
import logging
import json
logger = logging.getLogger(__name__)

logging.getLogger('requests').setLevel(logging.CRITICAL)

api_host = "http://18e777e3.ngrok.io"
api_key = "123"

headers = {
    "x-api-key": api_key,
    "content-type": "application/json"
    }

def update_token(token_uid):

    path = "/broker/tokens/"
    url = api_host + path

    body = {
        "id": token_uid,
        "media_type": "YT",
        "duration": 20,
        "is_active": True
    }
    response = requests.post(url, data=json.dumps(body), headers=headers)
    response.raise_for_status()
    return response.status_code
