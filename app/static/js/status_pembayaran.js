let modalPembayaran = null;

document.addEventListener("DOMContentLoaded", () => {

    modalPembayaran = new bootstrap.Modal(
        document.getElementById("modalPembayaran")
    );

    document
        .getElementById("formPembayaran")
        .addEventListener("submit", simpanPembayaran);

    document
        .getElementById("searchPembayaran")
        .addEventListener("keyup", cariPembayaran);

});


// =====================================
// SEARCH
// =====================================

function cariPembayaran() {

    const keyword = document
        .getElementById("searchPembayaran")
        .value
        .toLowerCase();

    document
        .querySelectorAll("#tablePembayaran tr")
        .forEach(row => {

            row.style.display =
                row.innerText.toLowerCase().includes(keyword)
                    ? ""
                    : "none";

        });

}


// =====================================
// RESET FORM
// =====================================

function resetFormPembayaran() {

    document.getElementById("formPembayaran").reset();

    document.getElementById("id").value = "";

    document.getElementById("modalTitle").innerHTML =
        "Tambah Pembayaran";

}


// =====================================
// EDIT
// =====================================

async function editPembayaran(id) {

    try {

        const response =
            await fetch(`/api/status_pembayaran/${id}`);

        if (!response.ok) {

            throw new Error("Gagal mengambil data");

        }

        const data = await response.json();

        document.getElementById("id").value = data.id;

        document.getElementById("anggota_id").value =
            data.anggota_id;

        document.getElementById("bulan").value =
            data.bulan;

        document.getElementById("tahun").value =
            data.tahun;

        document.getElementById("nominal").value =
            data.nominal;

        document.getElementById("tanggal_bayar").value =
            data.tanggal_bayar;

        document.getElementById("status").value =
            data.status;

        document.getElementById("keterangan").value =
            data.keterangan ?? "";

        document.getElementById("modalTitle").innerHTML =
            "Edit Pembayaran";

        modalPembayaran.show();

    }
    catch (err) {

        Swal.fire(
            "Error",
            err.message,
            "error"
        );

    }

}


// =====================================
// SIMPAN
// =====================================

async function simpanPembayaran(event) {

    event.preventDefault();

    const id =
        document.getElementById("id").value;

    const payload = {

        anggota_id: parseInt(
            document.getElementById("anggota_id").value
        ),

        bulan:
            document.getElementById("bulan").value,

        tahun: parseInt(
            document.getElementById("tahun").value
        ),

        nominal: parseInt(
            document.getElementById("nominal").value
        ),

        tanggal_bayar:
            document.getElementById("tanggal_bayar").value,

        status:
            document.getElementById("status").value,

        keterangan:
            document.getElementById("keterangan").value

    };

    const url =
        id
            ? `/api/status_pembayaran/${id}`
            : "/api/status_pembayaran/";

    const method =
        id
            ? "PUT"
            : "POST";

    try {

        const response = await fetch(url, {

            method,

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(payload)

        });

        const result = await response.json();

        if (!response.ok) {

            throw new Error(
                result.detail || "Terjadi kesalahan"
            );

        }

        Swal.fire({

            icon: "success",

            title: "Berhasil",

            text: "Data berhasil disimpan",

            timer: 1500,

            showConfirmButton: false

        }).then(() => {

            location.reload();

        });

    }
    catch (err) {

        Swal.fire(
            "Error",
            err.message,
            "error"
        );

    }

}


// =====================================
// DELETE
// =====================================

async function hapusPembayaran(id) {

    const konfirmasi =
        await Swal.fire({

            title: "Hapus data?",

            text: "Data yang dihapus tidak dapat dikembalikan.",

            icon: "warning",

            showCancelButton: true,

            confirmButtonText: "Ya",

            cancelButtonText: "Batal"

        });

    if (!konfirmasi.isConfirmed) {

        return;

    }

    try {

        const response =
            await fetch(`/api/status_pembayaran/${id}`, {

                method: "DELETE"

            });

        const result =
            await response.json();

        if (!response.ok) {

            throw new Error(
                result.detail || "Gagal menghapus data"
            );

        }

        Swal.fire({

            icon: "success",

            title: "Berhasil",

            text: "Data berhasil dihapus",

            timer: 1500,

            showConfirmButton: false

        }).then(() => {

            location.reload();

        });

    }
    catch (err) {

        Swal.fire(
            "Error",
            err.message,
            "error"
        );

    }

}