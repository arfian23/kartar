from datetime import date, time, datetime
from typing import Optional

from pydantic import BaseModel


class AgendaCreate(BaseModel):
    judul: str
    deskripsi: Optional[str] = None
    tanggal: date
    waktu: time
    lokasi: str
    status: str = "Akan Datang"


class AgendaUpdate(BaseModel):
    judul: str
    deskripsi: Optional[str] = None
    tanggal: date
    waktu: time
    lokasi: str
    status: str


class AgendaResponse(BaseModel):
    id: int
    judul: str
    deskripsi: Optional[str]
    tanggal: date
    waktu: time
    lokasi: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True