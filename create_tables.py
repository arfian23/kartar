from app.database.database import Base, engine

# Import semua model
from app.models.user import User
from app.models.anggota import Anggota
from app.models.kas_masuk import KasMasuk
from app.models.kas_keluar import KasKeluar

print("Membuat tabel...")

Base.metadata.create_all(bind=engine)

print("Semua tabel berhasil dibuat!")