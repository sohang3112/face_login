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

def jpeg_image_from_url(url: str) -> Image:
    return image_from_base64(url.removeprefix('data:image/jpeg;base64,'))

def face_encoding_from_image(img: Image):
    return fc.face_encodings(np.array(img))[0]

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# FIXME - in a real app, this should be replaced with a database
users = []    # [ { username, data, face_encoding } ]

@app.get('/')
async def index():
    return FileResponse('static/index.html')

@app.post('/register')
async def register(req: Request):
    # TODO - check that it doesn't already exist!
    json = await req.json()
    username = json['username']
    enc = face_encoding_from_image(jpeg_image_from_url(json['imageUrl']))
    users.append({'username': username, 'data': '', 'face_encoding': enc})

@app.post('/login')
async def login(req: Request):
    json = await req.json()
    user_enc = face_encoding_from_image(image_from_url(json['imageUrl']))
    user_face_encodings = [user['face_encoding'] for user in users]
    matches = np.where(fc.face_distance(user_face_encodings, user_enc) <= FACE_DISTANCE_TOLERANCE)[0]
    if matches.size == 0:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, headers = { 'WWW-Authenticate': 'Bearer' })
    assert matches.size == 1, 'Only 1 face should match'
    user = users[matches[0]]
    return {
        'username': user['username'],
        'data': user['data']
    }
    