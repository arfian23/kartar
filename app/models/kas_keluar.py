from sqlalchemy import Column, Integer, String, BigInteger, Date, DateTime
from sqlalchemy.sql import func

from app.database.database import Base


class KasKeluar(Base):
    __tablename__ = "kas_keluar"

    id = Column(Integer, primary_key=True, index=True)

    tanggal = Column(Date, nullable=False)

    kategori = Column(String(100), nullable=False)

    keperluan = Column(String(255), nullable=False)

    nominal = Column(BigInteger, nullable=False)

    keterangan = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())