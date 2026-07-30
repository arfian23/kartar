from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.agenda import Agenda

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


def user_session(request: Request):
    return {
        "id": request.session.get("user_id"),
        "nama": request.session.get("nama"),
        "role": request.session.get("role"),
    }


@router.get("/agenda", response_class=HTMLResponse)
def halaman_agenda(request: Request):

    if "user_id" not in request.session:

        return RedirectResponse(
            url="/login",
            status_code=302
        )

    db: Session = SessionLocal()

    agenda = (
        db.query(Agenda)
        .order_by(
            Agenda.tanggal.asc(),
            Agenda.waktu.asc()
        )
        .all()
    )

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="agenda.html",
        context={
            "user": user_session(request),
            "agenda_list": agenda,
        }
    )