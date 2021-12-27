# Login using Face Detection (Prototype)
Web-based Prototype for Login using Face Detection & Matching.

## Pre-Requisites
- Python 3 and Pip must be installed and available on environment PATH.
- Install uvicorn : `pip install uvicorn`. Make sure it is available on the environment PATH.

## Installation & Running
```
git clone https://github.com/sohang3112/face_login.git   # Clone this repository
cd face_login
pip install -r requirements.txt

# Run the server using uvicorn
uvicorn main:app
```

- After starting server by following these instructions, open http://localhost:8000 in your browser.
- A browser popup should show, asking for WebCam access. Click Allow.
- Your webcam will show on screen. 
- Ensure proper lighting. There should be no other face in front of your webcam.
- Click Login button. 
- You will be prompted to register as a new user. Enter your new username in prompt window and click Enter.
- Now you are registered. The next time you click on Login, there will be a popup saying "You are Registered!"


