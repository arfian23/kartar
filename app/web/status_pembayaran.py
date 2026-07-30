from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.status_pembayaran import StatusPembayaran
from app.models.anggota import Anggota

router = APIRouter()
templates = Jinja2Templates(
    directory="app/templates"
)

# =====================================
# HELPER
# =====================================
def cek_login(request: Request):

    if "user_id" not in request.session:
        return None

    return request.session


def cek_role(user):

    return user["role"] in [
        "ketua",
        "wakil",
        "bendahara"
    ]


# =====================================
# HALAMAN STATUS PEMBAYARAN
# =====================================
@router.get("/status_pembayaran")
def halaman_status_pembayaran(request: Request):

    user = cek_login(request)

    if not user:
        return RedirectResponse("/login", status_code=302)

    if not cek_role(user):
        return RedirectResponse("/", status_code=302)

    db: Session = SessionLocal()

    try:

        pembayaran_list = (
            db.query(StatusPembayaran)
            .join(Anggota)
            .order_by(
                StatusPembayaran.tahun.desc(),
                StatusPembayaran.bulan.asc(),
                Anggota.nama.asc()
            )
            .all()
        )

        anggota_list = (
            db.query(Anggota)
            .order_by(Anggota.nama.asc())
            .all()
        )

        return templates.TemplateResponse(
            request=request,
            name="status_pembayaran.html",
            context={
                "request": request,
                "user": user,
                "pembayaran_list": pembayaran_list,
                "anggota_list": anggota_list,
            }
        )

    finally:
        db.close()