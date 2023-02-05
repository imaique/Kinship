from fastapi import FastAPI
from pydantic import BaseModel
import base64

app = FastAPI()


class UserInfo(BaseModel):
    Name: str
    Image: str


@app.post('/')
async def upload_info_endpoint(userinfo: UserInfo):
    img_data = bytes(userinfo.Image, encoding="ascii")
    with open("imageToSave.png", "wb") as fh:
        fh.write(base64.decodebytes(img_data))

    return userinfo
