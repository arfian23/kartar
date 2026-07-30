from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Anggota(Base):
    __tablename__ = "anggota"

    id = Column(Integer, primary_key=True, index=True)

    nama = Column(String(150), nullable=False)

    rt = Column(String(20), nullable=False)

    no_hp = Column(String(20))

    alamat = Column(String(255))

    status = Column(String(20), default="Aktif")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # ==========================
    # RELATIONSHIP
    # ==========================
    status_pembayaran = relationship(
        "StatusPembayaran",
        back_populates="anggota",
        cascade="all, delete-orphan"
    )