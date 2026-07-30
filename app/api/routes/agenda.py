from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.agenda import Agenda
from app.schemas.agenda import (
    AgendaCreate,
    AgendaUpdate,
    AgendaResponse,
)

router = APIRouter(
    prefix="/api/agenda",
    tags=["Agenda"],
)


# =====================================
# CREATE AGENDA
# =====================================
@router.post("/", response_model=AgendaResponse)
def tambah_agenda(
    data: AgendaCreate,
    db: Session = Depends(get_db)
):

    agenda = Agenda(
        judul=data.judul,
        deskripsi=data.deskripsi,
        tanggal=data.tanggal,
        waktu=data.waktu,
        lokasi=data.lokasi,
        status=data.status,
    )

    db.add(agenda)
    db.commit()
    db.refresh(agenda)

    return agenda


# =====================================
# GET ALL AGENDA
# =====================================
@router.get("/", response_model=list[AgendaResponse])
def semua_agenda(
    db: Session = Depends(get_db)
):

    return (
        db.query(Agenda)
        .order_by(Agenda.tanggal.asc(), Agenda.waktu.asc())
        .all()
    )


# =====================================
# GET AGENDA BY ID
# =====================================
@router.get("/{id}", response_model=AgendaResponse)
def detail_agenda(
    id: int,
    db: Session = Depends(get_db)
):

    agenda = (
        db.query(Agenda)
        .filter(Agenda.id == id)
        .first()
    )

    if not agenda:

        raise HTTPException(
            status_code=404,
            detail="Agenda tidak ditemukan"
        )

    return agenda


# =====================================
# UPDATE AGENDA
# =====================================
@router.put("/{id}", response_model=AgendaResponse)
def edit_agenda(
    id: int,
    data: AgendaUpdate,
    db: Session = Depends(get_db)
):

    agenda = (
        db.query(Agenda)
        .filter(Agenda.id == id)
        .first()
    )

    if not agenda:

        raise HTTPException(
            status_code=404,
            detail="Agenda tidak ditemukan"
        )

    agenda.judul = data.judul
    agenda.deskripsi = data.deskripsi
    agenda.tanggal = data.tanggal
    agenda.waktu = data.waktu
    agenda.lokasi = data.lokasi
    agenda.status = data.status

    db.commit()
    db.refresh(agenda)

    return agenda


# =====================================
# DELETE AGENDA
# =====================================
@router.delete("/{id}")
def hapus_agenda(
    id: int,
    db: Session = Depends(get_db)
):

    agenda = (
        db.query(Agenda)
        .filter(Agenda.id == id)
        .first()
    )

    if not agenda:

        raise HTTPException(
            status_code=404,
            detail="Agenda tidak ditemukan"
        )

    db.delete(agenda)
    db.commit()

    return {
        "message": "Agenda berhasil dihapus"
    }