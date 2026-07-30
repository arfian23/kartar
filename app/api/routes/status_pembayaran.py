from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.status_pembayaran import StatusPembayaran
from app.schemas.status_pembayaran import (
    StatusPembayaranCreate,
    StatusPembayaranUpdate,
    StatusPembayaranResponse,
)

router = APIRouter(
    prefix="/api/status_pembayaran",
    tags=["Status Pembayaran"],
)


# =====================================
# CREATE STATUS PEMBAYARAN
# =====================================
@router.post("/", response_model=StatusPembayaranResponse)
def tambah_status_pembayaran(
    data: StatusPembayaranCreate,
    db: Session = Depends(get_db)
):

    pembayaran = StatusPembayaran(
        anggota_id=data.anggota_id,
        bulan=data.bulan,
        tahun=data.tahun,
        nominal=data.nominal,
        tanggal_bayar=data.tanggal_bayar,
        status=data.status,
        keterangan=data.keterangan,
    )

    db.add(pembayaran)
    db.commit()
    db.refresh(pembayaran)

    return pembayaran


# =====================================
# GET ALL STATUS PEMBAYARAN
# =====================================
@router.get("/", response_model=list[StatusPembayaranResponse])
def semua_status_pembayaran(
    db: Session = Depends(get_db)
):

    return (
        db.query(StatusPembayaran)
        .order_by(
            StatusPembayaran.tahun.desc(),
            StatusPembayaran.bulan.asc(),
            StatusPembayaran.id.desc(),
        )
        .all()
    )


# =====================================
# GET STATUS PEMBAYARAN BY ID
# =====================================
@router.get("/{id}", response_model=StatusPembayaranResponse)
def detail_status_pembayaran(
    id: int,
    db: Session = Depends(get_db)
):

    pembayaran = (
        db.query(StatusPembayaran)
        .filter(StatusPembayaran.id == id)
        .first()
    )

    if not pembayaran:
        raise HTTPException(
            status_code=404,
            detail="Data pembayaran tidak ditemukan"
        )

    return pembayaran


# =====================================
# UPDATE STATUS PEMBAYARAN
# =====================================
@router.put("/{id}", response_model=StatusPembayaranResponse)
def edit_status_pembayaran(
    id: int,
    data: StatusPembayaranUpdate,
    db: Session = Depends(get_db)
):

    pembayaran = (
        db.query(StatusPembayaran)
        .filter(StatusPembayaran.id == id)
        .first()
    )

    if not pembayaran:
        raise HTTPException(
            status_code=404,
            detail="Data pembayaran tidak ditemukan"
        )

    pembayaran.anggota_id = data.anggota_id
    pembayaran.bulan = data.bulan
    pembayaran.tahun = data.tahun
    pembayaran.nominal = data.nominal
    pembayaran.tanggal_bayar = data.tanggal_bayar
    pembayaran.status = data.status
    pembayaran.keterangan = data.keterangan

    db.commit()
    db.refresh(pembayaran)

    return pembayaran


# =====================================
# DELETE STATUS PEMBAYARAN
# =====================================
@router.delete("/{id}")
def hapus_status_pembayaran(
    id: int,
    db: Session = Depends(get_db)
):

    pembayaran = (
        db.query(StatusPembayaran)
        .filter(StatusPembayaran.id == id)
        .first()
    )

    if not pembayaran:
        raise HTTPException(
            status_code=404,
            detail="Data pembayaran tidak ditemukan"
        )

    db.delete(pembayaran)
    db.commit()

    return {
        "message": "Data pembayaran berhasil dihapus"
    }