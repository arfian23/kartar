const API_URL = "/kas_keluar";

async function simpanKasKeluar() {

    const kasId = document.getElementById("kas_id").value;

    const data = {

        tanggal: document.getElementById("tanggal").value,

        kategori: document.getElementById("kategori").value,

        keperluan: document.getElementById("keperluan").value,

        nominal: parseInt(document.getElementById("nominal").value),

        keterangan: document.getElementById("keterangan").value

    };

    if (
        !data.tanggal ||
        !data.kategori ||
        !data.keperluan ||
        !data.nominal
    ) {

        Swal.fire(
            "Peringatan",
            "Semua data wajib diisi!",
            "warning"
        );

        return;

    }

    let url = API_URL + "/";
    let method = "POST";

    if (kasId !== "") {

        url = API_URL + "/" + kasId;
        method = "PUT";

    }

    const response = await fetch(url, {

        method: method,

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)

    });

    if (response.ok) {

        Swal.fire({

            icon: "success",
            title: "Berhasil",
            text: "Data berhasil disimpan"

        }).then(() => {

            location.reload();

        });

    } else {

        Swal.fire(
            "Gagal",
            "Data gagal disimpan",
            "error"
        );

    }

}


async function editKasKeluar(id) {

    const response = await fetch(API_URL + "/" + id);

    const data = await response.json();

    document.getElementById("kas_id").value = data.id;

    document.getElementById("tanggal").value = data.tanggal;

    document.getElementById("kategori").value = data.kategori;

    document.getElementById("keperluan").value = data.keperluan;

    document.getElementById("nominal").value = data.nominal;

    document.getElementById("keterangan").value = data.keterangan;

    const modal = new bootstrap.Modal(
        document.getElementById("modalKasKeluar")
    );

    modal.show();

}


async function hapusKasKeluar(id) {

    const result = await Swal.fire({

        title: "Hapus Data?",

        text: "Data tidak bisa dikembalikan.",

        icon: "warning",

        showCancelButton: true,

        confirmButtonText: "Ya",

        cancelButtonText: "Batal"

    });

    if (!result.isConfirmed) {

        return;

    }

    const response = await fetch(API_URL + "/" + id, {

        method: "DELETE"

    });

    if (response.ok) {

        Swal.fire({

            icon: "success",

            title: "Berhasil",

            text: "Data berhasil dihapus"

        }).then(() => {

            location.reload();

        });

    } else {

        Swal.fire(
            "Gagal",
            "Data gagal dihapus",
            "error"
        );

    }

}