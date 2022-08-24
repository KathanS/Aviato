import requests
from PIL import Image
import json
from io import StringIO, BytesIO

WOMBO_KEY = "AIzaSyDCvp5MTJLUdtBYEKYWXJrlLzu1zuKM6Xw"

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
    im.save("out.png")

def generate_picture(prompt: str, style: int = 5):
    img_uri = __getImgUrl(__sign_up(WOMBO_KEY), prompt, style)
    __img(img_uri)