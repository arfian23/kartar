from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.models.user import User
from app.models.anggota import Anggota

from app.core.security import (
    verify_password,
    hash_password
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter()


# ============================================================
# TEMPLATE
# ============================================================

templates = Jinja2Templates(
    directory="app/templates"
)


# ============================================================
# LOGIN PAGE
# ============================================================

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


# ============================================================
# LOGIN
# ============================================================

@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    db: Session = SessionLocal()

    try:

        # ====================================================
        # CARI USER
        # ====================================================

        user = (
            db.query(User)
            .filter(
                User.username == username
            )
            .first()
        )


        # ====================================================
        # USERNAME TIDAK DITEMUKAN
        # ====================================================

        if user is None:

            return templates.TemplateResponse(
                request=request,
                name="login.html",
                context={
                    "error":
                        "Username tidak ditemukan"
                }
            )


        # ====================================================
        # AKUN TIDAK AKTIF
        # ====================================================

        if not user.status:

            return templates.TemplateResponse(
                request=request,
                name="login.html",
                context={
                    "error":
                        "Akun Anda belum aktif."
                }
            )


        # ====================================================
        # PASSWORD SALAH
        # ====================================================

        if not verify_password(
            password,
            user.password
        ):

            return templates.TemplateResponse(
                request=request,
                name="login.html",
                context={
                    "error":
                        "Password salah"
                }
            )


        # ====================================================
        # SIMPAN SESSION
        # ====================================================

        request.session["user_id"] = (
            user.id
        )

        request.session["nama"] = (
            user.nama_lengkap
        )

        request.session["role"] = (
            user.role
        )


        # ====================================================
        # REDIRECT DASHBOARD
        # ====================================================

        return RedirectResponse(
            url="/",
            status_code=302
        )


    finally:

        db.close()


# ============================================================
# REGISTER PAGE
# ============================================================

@router.get("/register")
def register_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


# ============================================================
# REGISTER
# ============================================================

@router.post("/register")
def register(
    request: Request,

    # Data anggota
    nama: str = Form(...),
    rt: str = Form(...),
    no_hp: str = Form(...),
    alamat: str = Form(...),

    # Data akun
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):

    db: Session = SessionLocal()

    try:

        # ====================================================
        # BERSIHKAN INPUT
        # ====================================================

        nama = nama.strip()

        rt = rt.strip()

        no_hp = no_hp.strip()

        alamat = alamat.strip()

        username = username.strip()


        # ====================================================
        # VALIDASI INPUT KOSONG
        # ====================================================

        if not nama:

            return templates.TemplateResponse(
                request=request,
                name="register.html",
                context={
                    "error":
                        "Nama lengkap wajib diisi."
                }
            )


        if not rt:

            return templates.TemplateResponse(
                request=request,
                name="register.html",
                context={
                    "error":
                        "RT wajib diisi."
                }
            )


        if not username:

            return templates.TemplateResponse(
                request=request,
                name="register.html",
                context={
                    "error":
                        "Username wajib diisi."
                }
            )


        # ====================================================
        # PASSWORD TIDAK SAMA
        # ====================================================

        if password != confirm_password:

            return templates.TemplateResponse(
                request=request,
                name="register.html",
                context={
                    "error":
                        "Konfirmasi password tidak sesuai"
                }
            )


        # ====================================================
        # VALIDASI PANJANG PASSWORD
        # ====================================================

        if len(password) < 6:

            return templates.TemplateResponse(
                request=request,
                name="register.html",
                context={
                    "error":
                        "Password minimal 6 karakter."
                }
            )


        # ====================================================
        # CEK USERNAME
        # ====================================================

        cek_user = (
            db.query(User)
            .filter(
                User.username == username
            )
            .first()
        )


        if cek_user:

            return templates.TemplateResponse(
                request=request,
                name="register.html",
                context={
                    "error":
                        "Username sudah digunakan"
                }
            )


        # ====================================================
        # BUAT DATA ANGGOTA
        # ====================================================

        anggota_baru = Anggota(

            nama=nama,

            rt=rt,

            no_hp=no_hp,

            alamat=alamat,

            status="Aktif"
        )


        db.add(
            anggota_baru
        )


        # ====================================================
        # FLUSH
        #
        # Agar ID anggota langsung diperoleh tanpa commit.
        #
        # Contoh:
        #
        # anggota_baru.id = 1
        # ====================================================

        db.flush()


        # ====================================================
        # BUAT USER
        # ====================================================

        user_baru = User(

            username=username,

            password=hash_password(
                password
            ),

            nama_lengkap=nama,

            # Registrasi publik SELALU anggota
            role="anggota",

            # Langsung aktif
            status=True,

            # Otomatis terhubung
            anggota_id=anggota_baru.id
        )


        db.add(
            user_baru
        )


        # ====================================================
        # SIMPAN KEDUANYA
        # ====================================================

        db.commit()


        # ====================================================
        # REDIRECT LOGIN
        # ====================================================

        return RedirectResponse(
            url="/login?success=register",
            status_code=302
        )


    except Exception as error:

        # ====================================================
        # JIKA SALAH SATU GAGAL
        #
        # Anggota dan User sama-sama dibatalkan.
        # ====================================================

        db.rollback()

        print(
            f"ERROR REGISTER: {error}"
        )


        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "error":
                    "Registrasi gagal. Silakan coba kembali."
            }
        )


    finally:

        db.close()


# ============================================================
# LOGOUT
# ============================================================

@router.get("/logout")
def logout(
    request: Request
):

    request.session.clear()


    return RedirectResponse(
        "/login",
        status_code=302
    )