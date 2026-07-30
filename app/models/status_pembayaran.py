from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class StatusPembayaran(Base):
    __tablename__ = "status_pembayaran"

    id = Column(Integer, primary_key=True, index=True)

    anggota_id = Column(
        Integer,
        ForeignKey("anggota.id", ondelete="CASCADE"),
        nullable=False
    )

    bulan = Column(String(20), nullable=False)

    tahun = Column(Integer, nullable=False)

    nominal = Column(Integer, nullable=False)

    tanggal_bayar = Column(Date, nullable=False)

    status = Column(
        String(20),
        nullable=False,
        default="Belum Lunas"
    )

    keterangan = Column(String(255), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    anggota = relationship(
        "Anggota",
        back_populates="status_pembayaran"
    )