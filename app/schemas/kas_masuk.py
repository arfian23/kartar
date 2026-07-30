from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class KasMasukCreate(BaseModel):
    anggota_id: int
    tanggal: date
    bulan: str
    tahun: int
    nominal: int
    metode: str = "Cash"
    keterangan: Optional[str] = None


class KasMasukUpdate(BaseModel):
    anggota_id: int
    tanggal: date
    bulan: str
    tahun: int
    nominal: int
    metode: str
    keterangan: Optional[str] = None


class KasMasukResponse(BaseModel):
    id: int
    anggota_id: int
    tanggal: date
    bulan: str
    tahun: int
    nominal: int
    metode: str
    keterangan: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True