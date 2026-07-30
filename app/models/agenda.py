from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    Time,
    DateTime,
)
from sqlalchemy.sql import func

from app.database.database import Base


class Agenda(Base):
    __tablename__ = "agenda"

    id = Column(Integer, primary_key=True, index=True)

    judul = Column(String(200), nullable=False)

    deskripsi = Column(Text, nullable=True)

    tanggal = Column(Date, nullable=False)

    waktu = Column(Time, nullable=False)

    lokasi = Column(String(200), nullable=False)

    status = Column(
        String(30),
        nullable=False,
        default="Akan Datang"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )