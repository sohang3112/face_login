from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from PIL import Image
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import base64

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
async def index():
    return FileResponse('static/index.html')

@app.post('/login')
async def login(req: Request):
    data = await req.json()
    img_bytes = base64.decodebytes(bytes(data['imageUrl'].removeprefix('data:image/png;base64,'), 'ascii'))
    with open('image.png', 'wb') as f:
        f.write(img_bytes)
    print('Saved image')