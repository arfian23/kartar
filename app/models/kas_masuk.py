from sqlalchemy import Column, Integer, ForeignKey, Date, String, BigInteger, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class KasMasuk(Base):
    __tablename__ = "kas_masuk"

    id = Column(Integer, primary_key=True, index=True)

    anggota_id = Column(
        Integer,
        ForeignKey("anggota.id"),
        nullable=False
    )

    tanggal = Column(Date, nullable=False)

    bulan = Column(String(20), nullable=False)

    tahun = Column(Integer, nullable=False)

    nominal = Column(BigInteger, nullable=False)

    metode = Column(String(50), default="Cash")

    keterangan = Column(String(255))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relasi ke tabel anggota
    anggota = relationship("Anggota")