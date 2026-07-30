from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import joinedload

from app.database.database import SessionLocal
from app.models.anggota import Anggota
from app.models.kas_masuk import KasMasuk
from app.models.kas_keluar import KasKeluar
from app.models.user import User

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


def cek_login(request: Request):
    if "user_id" not in request.session:
        return RedirectResponse(
            url="/login",
            status_code=302
        )
    return None

def cek_role(request: Request, roles: list[str]):

    if "role" not in request.session:

        return RedirectResponse(
            url="/login",
            status_code=302
        )

    if request.session["role"] not in roles:

        return templates.TemplateResponse(
            request=request,
            name="403.html",
            context={
                "user": user_session(request),
                "message": "Anda tidak memiliki hak akses ke halaman ini."
            },
            status_code=403
        )

    return None

def user_session(request: Request):
    return {
        "id": request.session.get("user_id"),
        "nama": request.session.get("nama"),
        "role": request.session.get("role"),
    }


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):

    auth = cek_login(request)
    if auth:
        return auth

    db = SessionLocal()

    total_anggota = db.query(Anggota).count()

    total_kas_masuk = db.query(KasMasuk).all()
    total_kas_keluar = db.query(KasKeluar).all()

    jumlah_kas_masuk = sum(item.nominal for item in total_kas_masuk)
    jumlah_kas_keluar = sum(item.nominal for item in total_kas_keluar)

    saldo = jumlah_kas_masuk - jumlah_kas_keluar

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": user_session(request),
            "total_anggota": total_anggota,
            "saldo": saldo,
            "kas_masuk": jumlah_kas_masuk,
            "kas_keluar": jumlah_kas_keluar,
        },
    )


@router.get("/anggota", response_class=HTMLResponse)
def halaman_anggota(request: Request):

    auth = cek_login(request)
    if auth:
        return auth

    db = SessionLocal()

    anggota = db.query(Anggota).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="anggota.html",
        context={
            "user": user_session(request),
            "anggota_list": anggota,
        },
    )


@router.get("/users", response_class=HTMLResponse)
def halaman_users(request: Request):

    auth = cek_login(request)
    if auth:
        return auth

    izin = cek_role(request, ["ketua", "wakil"])
    if izin:
        return izin
    
    db = SessionLocal()

    users = (
        db.query(User)
        .order_by(User.id.desc())
        .all()
    )

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={
            "user": user_session(request),
            "user_list": users,
        },
    )


@router.get("/kas_masuk", response_class=HTMLResponse)
def halaman_kas_masuk(request: Request):

    auth = cek_login(request)
    if auth:
        return auth

    izin = cek_role(request, ["ketua", "wakil", "bendahara"])
    if izin:
        return izin

    db = SessionLocal()

    anggota = db.query(Anggota).order_by(Anggota.nama).all()

    kas_masuk = (
        db.query(KasMasuk)
        .options(joinedload(KasMasuk.anggota))
        .order_by(KasMasuk.tanggal.desc())
        .all()
    )

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="kas_masuk.html",
        context={
            "user": user_session(request),
            "anggota_list": anggota,
            "kas_masuk_list": kas_masuk,
        },
    )


@router.get("/kas_keluar", response_class=HTMLResponse)
def halaman_kas_keluar(request: Request):

    auth = cek_login(request)
    if auth:
        return auth

    izin = cek_role(request, ["ketua", "wakil", "bendahara"])
    if izin:
        return izin

    db = SessionLocal()

    kas_keluar = (
        db.query(KasKeluar)
        .order_by(KasKeluar.tanggal.desc())
        .all()
    )

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="kas_keluar.html",
        context={
            "user": user_session(request),
            "kas_keluar_list": kas_keluar,
        },
    )