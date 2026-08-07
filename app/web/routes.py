from datetime import date

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import joinedload
from sqlalchemy import func

from app.database.database import SessionLocal

from app.models.anggota import Anggota
from app.models.kas_masuk import KasMasuk
from app.models.kas_keluar import KasKeluar
from app.models.user import User
from app.models.agenda import Agenda


# ============================================================
# ROUTER
# ============================================================

router = APIRouter()


# ============================================================
# TEMPLATE
# ============================================================

templates = Jinja2Templates(
    directory="app/templates"
)


# ============================================================
# NAMA BULAN
# ============================================================

NAMA_BULAN = [
    "",
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember"
]


# ============================================================
# MAPPING BULAN KE NOMOR
# ============================================================

BULAN_KE_NOMOR = {
    "Januari": 1,
    "Februari": 2,
    "Maret": 3,
    "April": 4,
    "Mei": 5,
    "Juni": 6,
    "Juli": 7,
    "Agustus": 8,
    "September": 9,
    "Oktober": 10,
    "November": 11,
    "Desember": 12,
}


# ============================================================
# HELPER USER SESSION
# ============================================================

def user_session(request: Request):

    return {
        "id": request.session.get("user_id"),
        "nama": request.session.get("nama"),
        "role": request.session.get("role"),
    }


# ============================================================
# HELPER CEK LOGIN
# ============================================================

def cek_login(request: Request):

    if "user_id" not in request.session:

        return RedirectResponse(
            url="/login",
            status_code=302
        )

    return None


# ============================================================
# HELPER CEK ROLE
# ============================================================

def cek_role(
    request: Request,
    roles: list[str]
):

    if "role" not in request.session:

        return RedirectResponse(
            url="/login",
            status_code=302
        )

    if request.session["role"] not in roles:

        return templates.TemplateResponse(
            request=request,
            name="403.html",
            context={
                "user": user_session(request),
                "message":
                    "Anda tidak memiliki hak akses ke halaman ini."
            },
            status_code=403
        )

    return None


# ============================================================
# DASHBOARD
# ============================================================

@router.get(
    "/",
    response_class=HTMLResponse
)
def dashboard(
    request: Request,
    tahun: int | None = None
):

    # ========================================================
    # CEK LOGIN
    # ========================================================

    auth = cek_login(request)

    if auth:
        return auth


    db = SessionLocal()

    try:

        # ====================================================
        # SESSION
        # ====================================================

        user_id = request.session.get("user_id")
        role = request.session.get("role")


        # ====================================================
        # TANGGAL SEKARANG
        # ====================================================

        sekarang = date.today()

        tahun_saat_ini = sekarang.year
        bulan_saat_ini = sekarang.month

        nama_bulan_sekarang = (
            NAMA_BULAN[bulan_saat_ini]
        )


        # ====================================================
        # FILTER TAHUN STATUS KAS
        # ====================================================

        if tahun is None:

            tahun_filter = tahun_saat_ini

        else:

            tahun_filter = tahun


        # ====================================================
        # VALIDASI FILTER TAHUN
        # ====================================================

        if (
            tahun_filter < 2000
            or tahun_filter > tahun_saat_ini + 1
        ):

            tahun_filter = tahun_saat_ini


        # ====================================================
        # DAFTAR TAHUN FILTER
        # ====================================================

        daftar_tahun = list(
            range(
                tahun_saat_ini,
                tahun_saat_ini - 5,
                -1
            )
        )


        # ====================================================
        # DASHBOARD ANGGOTA
        # ====================================================

        if role == "anggota":

            # ================================================
            # AMBIL DATA USER
            # ================================================

            user_db = (
                db.query(User)
                .options(
                    joinedload(User.anggota)
                )
                .filter(
                    User.id == user_id
                )
                .first()
            )


            # ================================================
            # USER TIDAK DITEMUKAN
            # ================================================

            if not user_db:

                return RedirectResponse(
                    url="/logout",
                    status_code=302
                )


            anggota = user_db.anggota


            # ================================================
            # AGENDA MENDATANG
            # ================================================

            agenda_mendatang = (
                db.query(Agenda)
                .filter(
                    Agenda.tanggal >= sekarang
                )
                .order_by(
                    Agenda.tanggal.asc(),
                    Agenda.waktu.asc()
                )
                .limit(5)
                .all()
            )


            # ================================================
            # JUMLAH AGENDA
            # ================================================

            jumlah_agenda = (
                db.query(Agenda)
                .filter(
                    Agenda.tanggal >= sekarang
                )
                .count()
            )


            # ================================================
            # AKUN BELUM TERHUBUNG KE ANGGOTA
            # ================================================

            if anggota is None:

                return templates.TemplateResponse(
                    request=request,
                    name="dashboard_anggota.html",
                    context={

                        "user":
                            user_session(request),

                        "anggota":
                            None,

                        "belum_terhubung":
                            True,

                        "tahun_saat_ini":
                            tahun_saat_ini,

                        "bulan_saat_ini":
                            bulan_saat_ini,

                        "nama_bulan_sekarang":
                            nama_bulan_sekarang,

                        "tahun_filter":
                            tahun_filter,

                        "daftar_tahun":
                            daftar_tahun,

                        "status_bulan_ini":
                            "Belum Bayar",

                        "total_bulan_ini":
                            0,

                        "total_tahun_ini":
                            0,

                        "jumlah_bulan_lunas_tahun_ini":
                            0,

                        "jumlah_bulan_lunas_filter":
                            0,

                        "rekap_bulanan":
                            [],

                        "riwayat_pembayaran":
                            [],

                        "agenda_mendatang":
                            agenda_mendatang,

                        "jumlah_agenda":
                            jumlah_agenda,
                    }
                )


            # =================================================
            # PEMBAYARAN TAHUN AKTUAL
            #
            # PENTING:
            # Menggunakan KasMasuk.tahun,
            # BUKAN tahun dari KasMasuk.tanggal.
            # =================================================

            pembayaran_tahun_aktual = (
                db.query(KasMasuk)
                .filter(
                    KasMasuk.anggota_id
                    == anggota.id,

                    KasMasuk.tahun
                    == tahun_saat_ini
                )
                .order_by(
                    KasMasuk.tanggal.desc(),
                    KasMasuk.id.desc()
                )
                .all()
            )


            # =================================================
            # TOTAL KAS TAHUN AKTUAL
            # =================================================

            total_tahun_ini = sum(
                item.nominal
                for item
                in pembayaran_tahun_aktual
            )


            # =================================================
            # PEMBAYARAN BULAN AKTUAL
            #
            # Menggunakan kolom "bulan".
            # =================================================

            pembayaran_bulan_ini = [

                item

                for item
                in pembayaran_tahun_aktual

                if BULAN_KE_NOMOR.get(
                    item.bulan
                ) == bulan_saat_ini
            ]


            # =================================================
            # TOTAL BULAN AKTUAL
            # =================================================

            total_bulan_ini = sum(
                item.nominal
                for item
                in pembayaran_bulan_ini
            )


            # =================================================
            # STATUS BULAN AKTUAL
            # =================================================

            if total_bulan_ini > 0:

                status_bulan_ini = "Lunas"

            else:

                status_bulan_ini = "Belum Bayar"


            # =================================================
            # HITUNG JUMLAH BULAN LUNAS TAHUN AKTUAL
            # =================================================

            bulan_lunas_tahun_ini = set()


            for item in pembayaran_tahun_aktual:

                nomor_bulan = (
                    BULAN_KE_NOMOR.get(
                        item.bulan
                    )
                )


                if nomor_bulan:

                    bulan_lunas_tahun_ini.add(
                        nomor_bulan
                    )


            jumlah_bulan_lunas_tahun_ini = len(
                bulan_lunas_tahun_ini
            )


            # =================================================
            # PEMBAYARAN BERDASARKAN TAHUN FILTER
            #
            # Digunakan khusus Status Kas Saya.
            # =================================================

            pembayaran_tahun_filter = (
                db.query(KasMasuk)
                .filter(
                    KasMasuk.anggota_id
                    == anggota.id,

                    KasMasuk.tahun
                    == tahun_filter
                )
                .order_by(
                    KasMasuk.tanggal.asc(),
                    KasMasuk.id.asc()
                )
                .all()
            )


            # =================================================
            # MAPPING TOTAL PEMBAYARAN PER BULAN
            # =================================================

            pembayaran_per_bulan = {}


            for item in pembayaran_tahun_filter:

                # --------------------------------------------
                # Ambil nomor bulan berdasarkan kolom bulan
                # --------------------------------------------

                nomor_bulan = (
                    BULAN_KE_NOMOR.get(
                        item.bulan
                    )
                )


                # --------------------------------------------
                # Jika nama bulan tidak valid, lewati
                # --------------------------------------------

                if nomor_bulan is None:

                    continue


                # --------------------------------------------
                # Buat nilai awal
                # --------------------------------------------

                if (
                    nomor_bulan
                    not in pembayaran_per_bulan
                ):

                    pembayaran_per_bulan[
                        nomor_bulan
                    ] = 0


                # --------------------------------------------
                # Tambahkan nominal
                # --------------------------------------------

                pembayaran_per_bulan[
                    nomor_bulan
                ] += item.nominal


            # =================================================
            # REKAP JANUARI - DESEMBER
            # =================================================

            rekap_bulanan = []

            jumlah_bulan_lunas_filter = 0


            for nomor_bulan in range(1, 13):

                # --------------------------------------------
                # Total bulan
                # --------------------------------------------

                total_bulan = (
                    pembayaran_per_bulan.get(
                        nomor_bulan,
                        0
                    )
                )


                # --------------------------------------------
                # Status lunas
                # --------------------------------------------

                lunas = total_bulan > 0


                if lunas:

                    jumlah_bulan_lunas_filter += 1


                # ============================================
                # STATUS PEMBAYARAN
                # ============================================

                if lunas:

                    status = "lunas"


                # --------------------------------------------
                # Tahun masa depan
                # --------------------------------------------

                elif tahun_filter > tahun_saat_ini:

                    status = "belum_jatuh_tempo"


                # --------------------------------------------
                # Tahun sekarang tetapi bulan belum tiba
                # --------------------------------------------

                elif (
                    tahun_filter == tahun_saat_ini
                    and nomor_bulan > bulan_saat_ini
                ):

                    status = "belum_jatuh_tempo"


                # --------------------------------------------
                # Sudah jatuh tempo tetapi belum bayar
                # --------------------------------------------

                else:

                    status = "belum_bayar"


                # --------------------------------------------
                # Tambahkan ke rekap
                # --------------------------------------------

                rekap_bulanan.append({

                    "nomor":
                        nomor_bulan,

                    "nama":
                        NAMA_BULAN[
                            nomor_bulan
                        ],

                    "total":
                        total_bulan,

                    "lunas":
                        lunas,

                    "status":
                        status,
                })


            # =================================================
            # RIWAYAT PEMBAYARAN TERBARU
            #
            # Di sini tanggal memang digunakan karena kita
            # ingin mengetahui kapan pembayaran dilakukan.
            # =================================================

            riwayat_pembayaran = (
                db.query(KasMasuk)
                .filter(
                    KasMasuk.anggota_id
                    == anggota.id
                )
                .order_by(
                    KasMasuk.tanggal.desc(),
                    KasMasuk.id.desc()
                )
                .limit(5)
                .all()
            )


            # =================================================
            # TAMPILKAN DASHBOARD ANGGOTA
            # =================================================

            return templates.TemplateResponse(
                request=request,
                name="dashboard_anggota.html",
                context={

                    # -----------------------------------------
                    # USER
                    # -----------------------------------------

                    "user":
                        user_session(request),

                    "anggota":
                        anggota,

                    "belum_terhubung":
                        False,


                    # -----------------------------------------
                    # WAKTU AKTUAL
                    # -----------------------------------------

                    "tahun_saat_ini":
                        tahun_saat_ini,

                    "bulan_saat_ini":
                        bulan_saat_ini,

                    "nama_bulan_sekarang":
                        nama_bulan_sekarang,


                    # -----------------------------------------
                    # FILTER
                    # -----------------------------------------

                    "tahun_filter":
                        tahun_filter,

                    "daftar_tahun":
                        daftar_tahun,


                    # -----------------------------------------
                    # KAS BULAN INI
                    # -----------------------------------------

                    "status_bulan_ini":
                        status_bulan_ini,

                    "total_bulan_ini":
                        total_bulan_ini,


                    # -----------------------------------------
                    # KAS TAHUN INI
                    # -----------------------------------------

                    "total_tahun_ini":
                        total_tahun_ini,

                    "jumlah_bulan_lunas_tahun_ini":
                        jumlah_bulan_lunas_tahun_ini,


                    # -----------------------------------------
                    # STATUS KAS FILTER
                    # -----------------------------------------

                    "jumlah_bulan_lunas_filter":
                        jumlah_bulan_lunas_filter,

                    "rekap_bulanan":
                        rekap_bulanan,


                    # -----------------------------------------
                    # RIWAYAT
                    # -----------------------------------------

                    "riwayat_pembayaran":
                        riwayat_pembayaran,


                    # -----------------------------------------
                    # AGENDA
                    # -----------------------------------------

                    "agenda_mendatang":
                        agenda_mendatang,

                    "jumlah_agenda":
                        jumlah_agenda,
                }
            )


        # ====================================================
        # DASHBOARD PENGURUS
        # ====================================================

        total_anggota = (
            db.query(Anggota)
            .count()
        )


        # ====================================================
        # TOTAL SELURUH KAS MASUK
        # ====================================================

        jumlah_kas_masuk = (
            db.query(
                func.coalesce(
                    func.sum(
                        KasMasuk.nominal
                    ),
                    0
                )
            )
            .scalar()
        )


        # ====================================================
        # TOTAL SELURUH KAS KELUAR
        # ====================================================

        jumlah_kas_keluar = (
            db.query(
                func.coalesce(
                    func.sum(
                        KasKeluar.nominal
                    ),
                    0
                )
            )
            .scalar()
        )


        # ====================================================
        # SALDO
        # ====================================================

        saldo = (
            jumlah_kas_masuk
            - jumlah_kas_keluar
        )


        # ====================================================
        # TEMPLATE DASHBOARD PENGURUS
        # ====================================================

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={

                "user":
                    user_session(request),

                "total_anggota":
                    total_anggota,

                "saldo":
                    saldo,

                "kas_masuk":
                    jumlah_kas_masuk,

                "kas_keluar":
                    jumlah_kas_keluar,
            }
        )


    finally:

        db.close()


# ============================================================
# HALAMAN DATA ANGGOTA
# ============================================================

@router.get(
    "/anggota",
    response_class=HTMLResponse
)
def halaman_anggota(
    request: Request
):

    # ========================================================
    # CEK LOGIN
    # ========================================================

    auth = cek_login(request)

    if auth:
        return auth


    db = SessionLocal()

    try:

        anggota = (
            db.query(Anggota)
            .order_by(
                Anggota.nama.asc()
            )
            .all()
        )


        return templates.TemplateResponse(
            request=request,
            name="anggota.html",
            context={

                "user":
                    user_session(request),

                "anggota_list":
                    anggota,
            }
        )


    finally:

        db.close()


# ============================================================
# HALAMAN MANAJEMEN USER
# ============================================================

@router.get(
    "/users",
    response_class=HTMLResponse
)
def halaman_users(
    request: Request
):

    # ========================================================
    # CEK LOGIN
    # ========================================================

    auth = cek_login(request)

    if auth:
        return auth


    # ========================================================
    # CEK ROLE
    # ========================================================

    izin = cek_role(
        request,
        [
            "ketua",
            "wakil"
        ]
    )

    if izin:
        return izin


    db = SessionLocal()

    try:

        users = (
            db.query(User)
            .order_by(
                User.id.desc()
            )
            .all()
        )


        return templates.TemplateResponse(
            request=request,
            name="users.html",
            context={

                "user":
                    user_session(request),

                "user_list":
                    users,
            }
        )


    finally:

        db.close()


# ============================================================
# HALAMAN KAS MASUK
# ============================================================

@router.get(
    "/kas_masuk",
    response_class=HTMLResponse
)
def halaman_kas_masuk(
    request: Request
):

    # ========================================================
    # CEK LOGIN
    # ========================================================

    auth = cek_login(request)

    if auth:
        return auth


    # ========================================================
    # CEK ROLE
    # ========================================================

    izin = cek_role(
        request,
        [
            "ketua",
            "wakil",
            "bendahara"
        ]
    )

    if izin:
        return izin


    db = SessionLocal()

    try:

        # ====================================================
        # DATA ANGGOTA
        # ====================================================

        anggota = (
            db.query(Anggota)
            .order_by(
                Anggota.nama.asc()
            )
            .all()
        )


        # ====================================================
        # RIWAYAT KAS MASUK
        #
        # Diurutkan berdasarkan tanggal uang diterima.
        # ====================================================

        kas_masuk = (
            db.query(KasMasuk)
            .options(
                joinedload(
                    KasMasuk.anggota
                )
            )
            .order_by(
                KasMasuk.tanggal.desc(),
                KasMasuk.id.desc()
            )
            .all()
        )


        # ====================================================
        # DEFAULT FILTER
        # ====================================================

        sekarang = date.today()

        tahun_kas = sekarang.year

        bulan_awal = 1

        bulan_akhir = sekarang.month


        # ====================================================
        # AMBIL QUERY PARAMETER
        # ====================================================

        try:

            # -----------------------------------------------
            # Tahun
            # -----------------------------------------------

            if request.query_params.get("tahun"):

                tahun_kas = int(
                    request.query_params.get(
                        "tahun"
                    )
                )


            # -----------------------------------------------
            # Bulan awal
            # -----------------------------------------------

            if request.query_params.get(
                "bulan_awal"
            ):

                bulan_awal = int(
                    request.query_params.get(
                        "bulan_awal"
                    )
                )


            # -----------------------------------------------
            # Bulan akhir
            # -----------------------------------------------

            if request.query_params.get(
                "bulan_akhir"
            ):

                bulan_akhir = int(
                    request.query_params.get(
                        "bulan_akhir"
                    )
                )


        except (TypeError, ValueError):

            tahun_kas = sekarang.year

            bulan_awal = 1

            bulan_akhir = sekarang.month


        # ====================================================
        # VALIDASI TAHUN
        # ====================================================

        if (
            tahun_kas < 2000
            or tahun_kas > sekarang.year + 1
        ):

            tahun_kas = sekarang.year


        # ====================================================
        # VALIDASI BULAN AWAL
        # ====================================================

        if bulan_awal < 1:
            bulan_awal = 1

        if bulan_awal > 12:
            bulan_awal = 12


        # ====================================================
        # VALIDASI BULAN AKHIR
        # ====================================================

        if bulan_akhir < 1:
            bulan_akhir = 1

        if bulan_akhir > 12:
            bulan_akhir = 12


        # ====================================================
        # JIKA BULAN AWAL > BULAN AKHIR
        # ====================================================

        if bulan_awal > bulan_akhir:

            bulan_awal, bulan_akhir = (
                bulan_akhir,
                bulan_awal
            )


        # ====================================================
        # DAFTAR BULAN YANG DITAMPILKAN
        # ====================================================

        daftar_bulan = []


        for nomor in range(
            bulan_awal,
            bulan_akhir + 1
        ):

            daftar_bulan.append({

                "nomor":
                    nomor,

                "nama":
                    NAMA_BULAN[
                        nomor
                    ]
            })


        # ====================================================
        # PEMBAYARAN UNTUK REKAP
        #
        # PENTING:
        # Menggunakan KasMasuk.tahun,
        # bukan tahun dari tanggal transaksi.
        # ====================================================

        pembayaran_rekap = (
            db.query(KasMasuk)
            .filter(
                KasMasuk.tahun
                == tahun_kas
            )
            .all()
        )


        # ====================================================
        # MAPPING PEMBAYARAN
        #
        # Format:
        #
        # {
        #     (anggota_id, nomor_bulan): total
        # }
        # ====================================================

        pembayaran_map = {}


        for pembayaran in pembayaran_rekap:

            # -----------------------------------------------
            # Ambil nomor bulan berdasarkan kolom bulan
            # -----------------------------------------------

            nomor_bulan = (
                BULAN_KE_NOMOR.get(
                    pembayaran.bulan
                )
            )


            # -----------------------------------------------
            # Abaikan bulan yang tidak valid
            # -----------------------------------------------

            if nomor_bulan is None:

                continue


            # -----------------------------------------------
            # Hanya bulan sesuai filter
            # -----------------------------------------------

            if (
                nomor_bulan < bulan_awal
                or nomor_bulan > bulan_akhir
            ):

                continue


            # -----------------------------------------------
            # Key anggota + bulan
            # -----------------------------------------------

            key = (
                pembayaran.anggota_id,
                nomor_bulan
            )


            # -----------------------------------------------
            # Nilai awal
            # -----------------------------------------------

            if key not in pembayaran_map:

                pembayaran_map[key] = 0


            # -----------------------------------------------
            # Tambahkan nominal
            # -----------------------------------------------

            pembayaran_map[key] += (
                pembayaran.nominal
            )


        # ====================================================
        # REKAP PER ANGGOTA
        # ====================================================

        rekap_pembayaran = []


        for item_anggota in anggota:

            pembayaran_bulanan = {}


            for item_bulan in daftar_bulan:

                nomor_bulan = (
                    item_bulan["nomor"]
                )


                total = (
                    pembayaran_map.get(
                        (
                            item_anggota.id,
                            nomor_bulan
                        ),
                        0
                    )
                )


                pembayaran_bulanan[
                    nomor_bulan
                ] = total


            rekap_pembayaran.append({

                "anggota":
                    item_anggota,

                "pembayaran":
                    pembayaran_bulanan
            })


        # ====================================================
        # DAFTAR TAHUN FILTER
        # ====================================================

        daftar_tahun_kas = list(
            range(
                sekarang.year + 1,
                sekarang.year - 5,
                -1
            )
        )


        # ====================================================
        # TEMPLATE KAS MASUK
        # ====================================================

        return templates.TemplateResponse(
            request=request,
            name="kas_masuk.html",
            context={

                # -------------------------------------------
                # USER
                # -------------------------------------------

                "user":
                    user_session(request),


                # -------------------------------------------
                # DATA
                # -------------------------------------------

                "anggota_list":
                    anggota,

                "kas_masuk_list":
                    kas_masuk,


                # -------------------------------------------
                # FILTER
                # -------------------------------------------

                "tahun":
                    tahun_kas,

                "bulan_awal":
                    bulan_awal,

                "bulan_akhir":
                    bulan_akhir,


                # -------------------------------------------
                # BULAN
                # -------------------------------------------

                "nama_bulan":
                    NAMA_BULAN,

                "daftar_bulan":
                    daftar_bulan,


                # -------------------------------------------
                # TAHUN
                # -------------------------------------------

                "daftar_tahun":
                    daftar_tahun_kas,


                # -------------------------------------------
                # REKAP
                # -------------------------------------------

                "rekap_pembayaran":
                    rekap_pembayaran,
            }
        )


    finally:

        db.close()


# ============================================================
# HALAMAN KAS KELUAR
# ============================================================

@router.get(
    "/kas_keluar",
    response_class=HTMLResponse
)
def halaman_kas_keluar(
    request: Request
):

    # ========================================================
    # CEK LOGIN
    # ========================================================

    auth = cek_login(request)

    if auth:
        return auth


    # ========================================================
    # CEK ROLE
    # ========================================================

    izin = cek_role(
        request,
        [
            "ketua",
            "wakil",
            "bendahara"
        ]
    )

    if izin:
        return izin


    db = SessionLocal()

    try:

        # ====================================================
        # DATA KAS KELUAR
        # ====================================================

        kas_keluar = (
            db.query(KasKeluar)
            .order_by(
                KasKeluar.tanggal.desc(),
                KasKeluar.id.desc()
            )
            .all()
        )


        # ====================================================
        # TEMPLATE
        # ====================================================

        return templates.TemplateResponse(
            request=request,
            name="kas_keluar.html",
            context={

                "user":
                    user_session(request),

                "kas_keluar_list":
                    kas_keluar,
            }
        )


    finally:

        db.close()