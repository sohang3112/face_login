from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import FileResponse
from PIL import Image
from io import BytesIO
import base64

def image_from_base64(string: str) -> Image:
    img_bytes = base64.decodebytes(bytes(string, 'ascii'))
    return Image.open(BytesIO(img_bytes))

class LoginImage(BaseModel):
    url: str

    def to_pillow_image(self) -> Image:
        return image_from_base64(self.url.removeprefix('data:image/png;base64,'))

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
async def index():
    return FileResponse('static/index.html')

@app.post('/login')
async def login(login_img: LoginImage):
    img = login_img.to_pillow_image()
    