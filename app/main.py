from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.database.database import Base, engine

# ==========================
# API
# ==========================
from app.api.routes.anggota import router as anggota_router
from app.api.routes.kas_masuk import router as kas_masuk_router
from app.api.routes.kas_keluar import router as kas_keluar_router
from app.api.routes.users import router as users_router
from app.api.routes.agenda import router as agenda_router
from app.api.routes.status_pembayaran import router as status_pembayaran_router

# ==========================
# WEB
# ==========================
from app.web.routes import router as web_router
from app.web.auth import router as auth_router
from app.web.agenda import router as agenda_web_router
from app.web.status_pembayaran import router as status_pembayaran_web_router
from app.web.laporan import router as laporan_web_router


# ==========================
# FASTAPI
# ==========================
app = FastAPI(
    title="Karang Taruna Sendangan",
    version="1.0.0",
)


# ==========================
# DATABASE
# ==========================
Base.metadata.create_all(bind=engine)


# ==========================
# SESSION
# ==========================
app.add_middleware(
    SessionMiddleware,
    secret_key="karangtaruna-secret-key-ganti-dengan-random-yang-panjang"
)


# ==========================
# STATIC FILE
# ==========================
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


# ==========================
# API ROUTER
# ==========================
app.include_router(anggota_router)
app.include_router(kas_masuk_router)
app.include_router(kas_keluar_router)
app.include_router(users_router)
app.include_router(agenda_router)
app.include_router(status_pembayaran_router)


# ==========================
# WEB ROUTER
# ==========================
app.include_router(auth_router)
app.include_router(web_router)
app.include_router(agenda_web_router)
app.include_router(status_pembayaran_web_router)
app.include_router(laporan_web_router)