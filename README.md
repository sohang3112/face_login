# Login using Face Detection (Prototype)
Web-based Prototype for Login using Face Detection & Matching.

## Pre-Requisites
- CMake must be installed (it is required by `dlib` Python package).
- Python 3 and Pip must be installed and available on environment PATH.

## Installation
```bash
git clone https://github.com/sohang3112/face_login.git   # Clone this repository
cd face_login

# This might take a while
# because building wheels for Python package dlib takes some time
pip install -r requirements.txt        
```

## Running
- Start the server using command `python -m uvicorn main:app` inside root directory of the repository.
- Open http://localhost:8000 in your browser.
- A browser popup should show, asking for WebCam access. Click Allow.
- Your webcam will show on screen. 
- Ensure proper lighting. There should be no other face in front of your webcam.
- Click Login button. 
- You will be prompted to register as a new user. Enter your new username in prompt window and click Enter.
- Now you are registered. The next time you click on Login, there will be a popup saying "You are Registered!"


