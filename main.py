from fastapi import FastAPI
from routers import users
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from utils.auth import generate_id
from dotenv import load_dotenv
import uvicorn
import os

load_dotenv()

PORT = int(os.getenv('PORT'))
WEB_URL = os.getenv('WEB_URL')

app = FastAPI(
    title="Sistem Alumni Asy Syaamil API",
    version="1.5.2",
)

app.include_router(users.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3333",
    f"http://{WEB_URL}",
    f"https://{WEB_URL}"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


image_dir_path = os.path.join(os.getcwd(), 'image')
if not os.path.exists(image_dir_path) and not os.path.isdir(image_dir_path):
    os.mkdir('image')

@app.get("/")
def home():
    return RedirectResponse("/docs")


@app.get('/generate-token')
def token():
    return generate_id(length=50)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)