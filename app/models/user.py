from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    nama_lengkap = Column(String(150), nullable=False)

    role = Column(String(30), nullable=False)

    status = Column(Boolean, default=True)

    anggota_id = Column(
        Integer,
        ForeignKey("anggota.id"),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    last_login = Column(
        DateTime(timezone=True),
        nullable=True
    )

    anggota = relationship("Anggota")