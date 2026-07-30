from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.kas_keluar import KasKeluar
from app.schemas.kas_keluar import (
    KasKeluarCreate,
    KasKeluarUpdate,
    KasKeluarResponse,
)

router = APIRouter(
    prefix="/kas_keluar",
    tags=["Kas Keluar"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=KasKeluarResponse)
def tambah_kas_keluar(
    data: KasKeluarCreate,
    db: Session = Depends(get_db),
):

    kas_keluar = KasKeluar(
        tanggal=data.tanggal,
        kategori=data.kategori,
        keperluan=data.keperluan,
        nominal=data.nominal,
        keterangan=data.keterangan,
    )

    db.add(kas_keluar)
    db.commit()
    db.refresh(kas_keluar)

    return kas_keluar


@router.get("/", response_model=list[KasKeluarResponse])
def semua_kas_keluar(
    db: Session = Depends(get_db),
):

    return (
        db.query(KasKeluar)
        .order_by(KasKeluar.tanggal.desc())
        .all()
    )


@router.get("/{kas_id}", response_model=KasKeluarResponse)
def detail_kas_keluar(
    kas_id: int,
    db: Session = Depends(get_db),
):

    kas_keluar = (
        db.query(KasKeluar)
        .filter(KasKeluar.id == kas_id)
        .first()
    )

    if not kas_keluar:
        raise HTTPException(
            status_code=404,
            detail="Data kas keluar tidak ditemukan",
        )

    return kas_keluar


@router.put("/{kas_id}", response_model=KasKeluarResponse)
def ubah_kas_keluar(
    kas_id: int,
    data: KasKeluarUpdate,
    db: Session = Depends(get_db),
):

    kas_keluar = (
        db.query(KasKeluar)
        .filter(KasKeluar.id == kas_id)
        .first()
    )

    if not kas_keluar:
        raise HTTPException(
            status_code=404,
            detail="Data kas keluar tidak ditemukan",
        )

    kas_keluar.tanggal = data.tanggal
    kas_keluar.kategori = data.kategori
    kas_keluar.keperluan = data.keperluan
    kas_keluar.nominal = data.nominal
    kas_keluar.keterangan = data.keterangan

    db.commit()
    db.refresh(kas_keluar)

    return kas_keluar


@router.delete("/{kas_id}")
def hapus_kas_keluar(
    kas_id: int,
    db: Session = Depends(get_db),
):

    kas_keluar = (
        db.query(KasKeluar)
        .filter(KasKeluar.id == kas_id)
        .first()
    )

    if not kas_keluar:
        raise HTTPException(
            status_code=404,
            detail="Data kas keluar tidak ditemukan",
        )

    db.delete(kas_keluar)
    db.commit()

    return {
        "message": "Data kas keluar berhasil dihapus"
    }