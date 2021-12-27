from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import FileResponse
import numpy as np
import face_recognition as fc
from PIL import Image
from io import BytesIO
import base64

FACE_DISTANCE_TOLERANCE = 0.6

def image_from_base64(string: str) -> Image:
    img_bytes = base64.decodebytes(bytes(string, 'ascii'))
    return Image.open(BytesIO(img_bytes))

def image_from_url(url: str) -> Image:
    return image_from_base64(url.removeprefix('data:image/jpeg;base64,'))

def face_encoding_from_image(img: Image):
    return fc.face_encodings(np.array(img))[0]

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

users = []    # [ (username, face_encoding) ]

@app.get('/')
async def index():
    return FileResponse('static/index.html')

@app.post('/register')
async def register(req: Request):
    # TODO - check that it doesn't already exist!
    json = await req.json()
    username = json['username']
    img = image_from_url(json['imageUrl'])
    enc = face_encoding_from_image(img)
    users.append((username, enc))

@app.post('/login')
async def login(req: Request):
    json = await req.json()
    url = json['imageUrl']
    img = image_from_url(url)
    breakpoint()
    user_enc = face_encoding_from_image(img)
    user_face_encodings = [enc for _, enc in users]
    matches = np.where(fc.face_distance(user_face_encodings, user_enc) <= FACE_DISTANCE_TOLERANCE)[0]
    if matches.size == 0:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, headers = { 'WWW-Authenticate': 'Bearer' })
    assert matches.size > 1, 'Only 1 face should match'
    return users[matches[0]]
    