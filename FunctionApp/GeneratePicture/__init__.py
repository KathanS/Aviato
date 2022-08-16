import logging

from click import prompt
import azure.functions as func
import requests
from PIL import Image
import json
from io import StringIO, BytesIO

import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

WOMBO_KEY = "AIzaSyDCvp5MTJLUdtBYEKYWXJrlLzu1zuKM6Xw"

def sign_up(key):
    body = {"key": key}
    r = requests.post(
        f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={key}",
        data=body,
    )
    id_token = r.json()["idToken"]
    return id_token
        
def getImgUrl(id_token: str, prompt: str, style: int):
    s = requests.Session()
    s.headers.update(
        {
            "Authorization": "bearer " + id_token,
            "Origin": "https://app.wombo.art",
            "Referer": "https://app.wombo.art/",
            "User-Agent": "Mozilla/5.0",
        }
    )
    
    def init_task():
        body = StringIO()
        json.dump({"premium": False}, body)
        r = s.post("https://paint.api.wombo.ai/api/tasks", data=body.getvalue())
        return r.json()["id"]

    id = init_task()

    body = (
        '{"input_spec":{"prompt":"'
        + prompt
        + '","style":'
        + str(style)
        + ',"display_freq":10}}'
    )
    
    r = s.put(f"https://paint.api.wombo.ai/api/tasks/{id}", data=body)
    
    result = s.post(f"https://app.wombo.art/api/tradingcard/{id}")
    img_uri = result.json()
    while not isinstance(img_uri, str):
        result = s.post(f"https://app.wombo.art/api/tradingcard/{id}")
        img_uri = result.json()

    return img_uri
    
def save_img(url):
    r = requests.get(url)
    im = Image.open(BytesIO(r.content))
    im = im.crop((65, 165, 950, 1510))

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    prompt = req.params.get('prompt')
    style = req.params.get('style')

    img_uri = getImgUrl(sign_up(WOMBO_KEY), prompt, style)
    save_img(img_uri)

    return func.HttpResponse("Image saved", status_code=200)