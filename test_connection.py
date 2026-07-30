from app.database.database import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("===================================")
        print("Berhasil terhubung ke Supabase!")
        print(result.fetchone()[0])
        print("===================================")

except Exception as e:
    print("Gagal koneksi!")
    print(e)