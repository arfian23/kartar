from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.kas_masuk import KasMasuk
from app.schemas.kas_masuk import (
    KasMasukCreate,
    KasMasukUpdate,
    KasMasukResponse
)

router = APIRouter(
    prefix="/kas_masuk",
    tags=["Kas Masuk"]
)


@router.post("/", response_model=KasMasukResponse)
def tambah_kas_masuk(
    data: KasMasukCreate,
    db: Session = Depends(get_db)
):

    kas = KasMasuk(
        anggota_id=data.anggota_id,
        tanggal=data.tanggal,
        bulan=data.bulan,
        tahun=data.tahun,
        nominal=data.nominal,
        metode=data.metode,
        keterangan=data.keterangan
    )

    db.add(kas)
    db.commit()
    db.refresh(kas)

    return kas


@router.get("/", response_model=list[KasMasukResponse])
def semua_kas_masuk(
    db: Session = Depends(get_db)
):

    return db.query(KasMasuk).all()


@router.get("/{id}", response_model=KasMasukResponse)
def detail_kas_masuk(
    id: int,
    db: Session = Depends(get_db)
):

    kas = db.query(KasMasuk).filter(
        KasMasuk.id == id
    ).first()

    if not kas:
        raise HTTPException(
            status_code=404,
            detail="Data tidak ditemukan"
        )

    return kas


@router.put("/{id}", response_model=KasMasukResponse)
def edit_kas_masuk(
    id: int,
    data: KasMasukUpdate,
    db: Session = Depends(get_db)
):

    kas = db.query(KasMasuk).filter(
        KasMasuk.id == id
    ).first()

    if not kas:
        raise HTTPException(
            status_code=404,
            detail="Data tidak ditemukan"
        )

    kas.anggota_id = data.anggota_id
    kas.tanggal = data.tanggal
    kas.bulan = data.bulan
    kas.tahun = data.tahun
    kas.nominal = data.nominal
    kas.metode = data.metode
    kas.keterangan = data.keterangan

    db.commit()
    db.refresh(kas)

    return kas


@router.delete("/{id}")
def hapus_kas_masuk(
    id: int,
    db: Session = Depends(get_db)
):

    kas = db.query(KasMasuk).filter(
        KasMasuk.id == id
    ).first()

    if not kas:
        raise HTTPException(
            status_code=404,
            detail="Data tidak ditemukan"
        )

    db.delete(kas)
    db.commit()

    return {
        "message": "Data berhasil dihapus"
    }