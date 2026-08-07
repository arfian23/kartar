from sqlalchemy import inspect, text

from app.database.database import engine


# ============================================================
# MENAMPILKAN SEMUA ISI DATABASE
# ============================================================

def tampilkan_database():

    inspector = inspect(engine)

    # Ambil semua nama tabel
    daftar_tabel = inspector.get_table_names()

    print("\n" + "=" * 80)
    print("ISI DATABASE KARANG TARUNA")
    print("=" * 80)

    print(f"\nJumlah tabel: {len(daftar_tabel)}")

    print("\nDaftar tabel:")

    for tabel in daftar_tabel:
        print(f"  - {tabel}")

    print("\n" + "=" * 80)

    # Membuka koneksi database
    with engine.connect() as connection:

        for nama_tabel in daftar_tabel:

            print("\n")
            print("=" * 80)
            print(f"TABEL: {nama_tabel}")
            print("=" * 80)

            # Ambil informasi kolom
            kolom = inspector.get_columns(nama_tabel)

            nama_kolom = [
                item["name"]
                for item in kolom
            ]

            # Query semua data
            hasil = connection.execute(
                text(
                    f'SELECT * FROM "{nama_tabel}" ORDER BY 1'
                )
            )

            rows = hasil.fetchall()

            # Jika tabel kosong
            if not rows:

                print("\n[TABEL KOSONG]")

                print("\nKolom:")

                for nama in nama_kolom:
                    print(f"  - {nama}")

                continue

            # ==================================================
            # HITUNG LEBAR KOLOM
            # ==================================================

            lebar = []

            for index, nama in enumerate(nama_kolom):

                panjang = len(str(nama))

                for row in rows:

                    nilai = row[index]

                    if nilai is None:
                        nilai = "NULL"

                    panjang = max(
                        panjang,
                        len(str(nilai))
                    )

                # Batasi supaya terminal tidak terlalu lebar
                lebar.append(
                    min(panjang, 30)
                )

            # ==================================================
            # HEADER
            # ==================================================

            header = " | ".join(

                str(nama_kolom[i])[
                    :lebar[i]
                ].ljust(lebar[i])

                for i in range(
                    len(nama_kolom)
                )
            )

            print()

            print(header)

            print("-" * len(header))

            # ==================================================
            # DATA
            # ==================================================

            for row in rows:

                data = []

                for index, nilai in enumerate(row):

                    if nilai is None:
                        nilai = "NULL"

                    nilai = str(nilai)

                    # Potong teks panjang
                    if len(nilai) > lebar[index]:

                        nilai = (
                            nilai[
                                :lebar[index] - 3
                            ]
                            + "..."
                        )

                    data.append(
                        nilai.ljust(
                            lebar[index]
                        )
                    )

                print(
                    " | ".join(data)
                )

            print(
                f"\nTotal data: {len(rows)}"
            )

    print("\n")
    print("=" * 80)
    print("SELESAI")
    print("=" * 80)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    try:

        tampilkan_database()

    except Exception as error:

        print("\nGAGAL MEMBACA DATABASE")

        print(f"Error: {error}")