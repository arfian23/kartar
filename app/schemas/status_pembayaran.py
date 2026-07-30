from datetime import date
from pydantic import BaseModel, ConfigDict


class StatusPembayaranBase(BaseModel):
    anggota_id: int
    bulan: str
    tahun: int
    nominal: int
    tanggal_bayar: date
    status: str
    keterangan: str | None = None


class StatusPembayaranCreate(StatusPembayaranBase):
    pass


class StatusPembayaranUpdate(StatusPembayaranBase):
    pass


class StatusPembayaranResponse(StatusPembayaranBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )