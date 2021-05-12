from fastapi import FastAPI 
from routers import users
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from utils.auth import generate_id

app = FastAPI()

app.include_router(users.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://sistem-alumni-asysyaamil-web.herokuapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return RedirectResponse("/docs")

@app.get('/generate-token')
def token():
    return generate_id(length=50)