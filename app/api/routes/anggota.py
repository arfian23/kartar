from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi import Query

from app.database.database import get_db
from app.models.anggota import Anggota
from app.schemas.anggota import (
    AnggotaCreate,
    AnggotaUpdate,
    AnggotaResponse,
)

router = APIRouter(
    prefix="/anggota",
    tags=["Anggota"],
)

@router.post("/", response_model=AnggotaResponse)
def tambah_anggota(data: AnggotaCreate, db: Session = Depends(get_db)):
    anggota = Anggota(
        nama=data.nama,
        rt=data.rt,
        no_hp=data.no_hp,
        alamat=data.alamat,
        status=data.status,
    )

    db.add(anggota)
    db.commit()
    db.refresh(anggota)

    return anggota

@router.get("/", response_model=list[AnggotaResponse])
def semua_anggota(db: Session = Depends(get_db)):
    return db.query(Anggota).all()

@router.get("/search")
def search_anggota(
    q: str = Query(..., min_length=2),
    db: Session = Depends(get_db)
):
    anggota = (
        db.query(Anggota)
        .filter(Anggota.nama.ilike(f"%{q}%"))
        .order_by(Anggota.nama.asc())
        .limit(10)
        .all()
    )

    return [
        {
            "id": item.id,
            "nama": item.nama,
            "rt": item.rt
        }
        for item in anggota
    ]

@router.get("/{id}", response_model=AnggotaResponse)
def detail_anggota(id: int, db: Session = Depends(get_db)):
    anggota = db.query(Anggota).filter(Anggota.id == id).first()

    if not anggota:
        raise HTTPException(
            status_code=404,
            detail="Anggota tidak ditemukan"
        )

    return anggota

@router.put("/{id}", response_model=AnggotaResponse)
def edit_anggota(
    id: int,
    data: AnggotaUpdate,
    db: Session = Depends(get_db)
):
    anggota = db.query(Anggota).filter(Anggota.id == id).first()

    if not anggota:
        raise HTTPException(
            status_code=404,
            detail="Anggota tidak ditemukan"
        )

    anggota.nama = data.nama
    anggota.rt = data.rt
    anggota.no_hp = data.no_hp
    anggota.alamat = data.alamat
    anggota.status = data.status

    db.commit()
    db.refresh(anggota)

    return anggota

@router.delete("/{id}")
def hapus_anggota(
    id: int,
    db: Session = Depends(get_db)
):
    anggota = db.query(Anggota).filter(Anggota.id == id).first()

    if not anggota:
        raise HTTPException(
            status_code=404,
            detail="Anggota tidak ditemukan"
        )

    db.delete(anggota)
    db.commit()

    return {
        "message": "Anggota berhasil dihapus"
    }

