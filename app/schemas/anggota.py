from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AnggotaCreate(BaseModel):
    nama: str
    rt: str
    no_hp: Optional[str] = None
    alamat: Optional[str] = None
    status: str = "Aktif"


class AnggotaUpdate(BaseModel):
    nama: str
    rt: str
    no_hp: Optional[str] = None
    alamat: Optional[str] = None
    status: str


class AnggotaResponse(BaseModel):
    id: int
    nama: str
    rt: str
    no_hp: Optional[str]
    alamat: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True