from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="Sistem Informasi Kas Karang Taruna",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def root():
    return {
        "message": "Selamat datang di Sistem Informasi Kas Karang Taruna"
    }