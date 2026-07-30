from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class KasKeluarCreate(BaseModel):
    tanggal: date
    kategori: str
    keperluan: str
    nominal: int
    keterangan: Optional[str] = None


class KasKeluarUpdate(BaseModel):
    tanggal: date
    kategori: str
    keperluan: str
    nominal: int
    keterangan: Optional[str] = None


class KasKeluarResponse(BaseModel):
    id: int
    tanggal: date
    kategori: str
    keperluan: str
    nominal: int
    keterangan: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)