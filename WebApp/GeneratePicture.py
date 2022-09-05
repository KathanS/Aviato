import requests
from PIL import Image
import json
from io import StringIO, BytesIO
import base64
import random

WOMBO_KEY = "AIzaSyDCvp5MTJLUdtBYEKYWXJrlLzu1zuKM6Xw"

STYLES = [[40,10,20,9],[48,16,6,1,28],[35,45,18,14],[2,21,11,17,34],[4,32,5,44]]

def hit():

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    response = requests.get('https://jsonblob.com/api/jsonBlob/1016218611752386560', headers=headers)

    curr = int(response.content.decode('ASCII'))

    headers = {
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    json_data = curr+1
    
    response = requests.put('https://jsonblob.com/api/jsonBlob/1016218611752386560', headers=headers, json=json_data)

def __sign_up(key):
    body = {"key": key}
    r = requests.post(
        f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={key}",
        data=body,
    )
    id_token = r.json()["idToken"]
    return id_token
        
def __getImgUrl(id_token: str, prompt: str, style: int):
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

    hit()

    r = s.put(f"https://paint.api.wombo.ai/api/tasks/{id}", data=body)
    
    result = s.post(f"https://app.wombo.art/api/tradingcard/{id}")
    img_uri = result.json()
    while not isinstance(img_uri, str):
        result = s.post(f"https://app.wombo.art/api/tradingcard/{id}")
        img_uri = result.json()

    return img_uri
    
def __img(url):
    r = requests.get(url)
    im = Image.open(BytesIO(r.content))
    im = im.crop((65, 165, 950, 1510))
    data = BytesIO()
    im.save(data, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())

    return encoded_img_data


def generate_picture(prompt: str, style: int = 5): # random group call
    style = random.choice(STYLES[style-1])
    img_uri = __getImgUrl(__sign_up(WOMBO_KEY), prompt, style)
    return __img(img_uri)