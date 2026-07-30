from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password, hash_password

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


# ==================================================
# LOGIN
# ==================================================

@router.get("/login")
def login_page(
    request: Request,
    success: str | None = None
):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "success": success
        }
    )


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    db: Session = SessionLocal()

    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if user is None:

        db.close()

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Username tidak ditemukan"
            }
        )

    # Akun belum diaktifkan
    if not user.status:

        db.close()

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Akun Anda belum diaktifkan oleh Ketua atau Wakil."
            }
        )

    if not verify_password(password, user.password):

        db.close()

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Password salah"
            }
        )

    request.session["user_id"] = user.id
    request.session["nama"] = user.nama_lengkap
    request.session["role"] = user.role

    db.close()

    return RedirectResponse(
        url="/",
        status_code=302
    )


# ==================================================
# REGISTER
# ==================================================

@router.get("/register")
def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


@router.post("/register")
def register(
    request: Request,
    nama: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):

    db: Session = SessionLocal()

    # Password tidak sama
    if password != confirm_password:

        db.close()

        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "error": "Konfirmasi password tidak sesuai"
            }
        )

    # Username sudah digunakan
    cek_user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if cek_user:

        db.close()

        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "error": "Username sudah digunakan"
            }
        )

    user = User(
        nama_lengkap=nama,
        username=username,
        password=hash_password(password),
        role="anggota",
        status=False
    )

    db.add(user)
    db.commit()

    db.close()

    return RedirectResponse(
        url="/login?success=register",
        status_code=302
    )


# ==================================================
# LOGOUT
# ==================================================

@router.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        "/login",
        status_code=302
    )