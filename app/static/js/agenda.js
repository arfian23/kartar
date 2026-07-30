document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("searchAgenda");
    if (searchInput) {
        searchInput.addEventListener("keyup", function () {
            const keyword = this.value.toLowerCase();
            const rows = document.querySelectorAll("#tbodyAgenda tr");

            rows.forEach(function (row) {
                row.style.display = row.innerText.toLowerCase().includes(keyword)
                    ? ""
                    : "none";
            });
        });
    }

    const modalAgenda = document.getElementById("modalAgenda");
    if (modalAgenda) {
        modalAgenda.addEventListener("hidden.bs.modal", function () {
            resetFormAgenda();
        });
    }

});

function resetFormAgenda() {
    document.getElementById("agenda_id").value = "";
    document.getElementById("judul").value = "";
    document.getElementById("deskripsi").value = "";
    document.getElementById("tanggal").value = "";
    document.getElementById("waktu").value = "";
    document.getElementById("lokasi").value = "";
    document.getElementById("status").value = "Akan Datang";

    const title = document.querySelector("#modalAgenda .modal-title");
    if (title) {
        title.innerText = "Tambah Agenda";
    }
}

async function editAgenda(id) {
    try {
        const response = await fetch(`/api/agenda/${id}`);

        if (!response.ok) {
            throw new Error("Gagal mengambil data");
        }

        const data = await response.json();

        document.getElementById("agenda_id").value = data.id;
        document.getElementById("judul").value = data.judul;
        document.getElementById("deskripsi").value = data.deskripsi ?? "";
        document.getElementById("tanggal").value = data.tanggal;
        document.getElementById("waktu").value =
            data.waktu ? data.waktu.substring(0, 5) : "";
        document.getElementById("lokasi").value = data.lokasi;
        document.getElementById("status").value = data.status;

        const title = document.querySelector("#modalAgenda .modal-title");
        if (title) {
            title.innerText = "Edit Agenda";
        }

        const modalElement = document.getElementById("modalAgenda");
        const modal = bootstrap.Modal.getOrCreateInstance(modalElement);
        modal.show();

    } catch (error) {
        Swal.fire("Error", "Gagal mengambil data agenda.", "error");
    }
}

async function simpanAgenda(event) {
    const btn = event?.currentTarget;

    const judul = document.getElementById("judul");
    const tanggal = document.getElementById("tanggal");
    const waktu = document.getElementById("waktu");
    const lokasi = document.getElementById("lokasi");
    const deskripsi = document.getElementById("deskripsi");

    if (
        !judul.value.trim() ||
        !tanggal.value ||
        !waktu.value ||
        !lokasi.value.trim()
    ) {
        Swal.fire("Peringatan", "Semua field wajib diisi.", "warning");
        return;
    }

    if (deskripsi.value.length > 500) {
        Swal.fire("Peringatan", "Deskripsi maksimal 500 karakter.", "warning");
        return;
    }

    const id = document.getElementById("agenda_id").value;

    const data = {
        judul: judul.value.trim(),
        deskripsi: deskripsi.value.trim(),
        tanggal: tanggal.value,
        waktu: waktu.value,
        lokasi: lokasi.value.trim(),
        status: document.getElementById("status").value
    };

    const url = id ? `/api/agenda/${id}` : "/api/agenda/";
    const method = id ? "PUT" : "POST";

    if (btn) {
        btn.disabled = true;
    }

    Swal.fire({
        title: "Menyimpan...",
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    try {
        const response = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        Swal.close();

        if (response.ok) {
            Swal.fire(
                "Berhasil",
                id ? "Agenda berhasil diperbarui." : "Agenda berhasil ditambahkan.",
                "success"
            ).then(() => {
                location.reload();
            });
        } else {
            let message = "Terjadi kesalahan.";

            try {
                const result = await response.json();
                message = result.detail || message;
            } catch (_) {}

            Swal.fire("Gagal", message, "error");
        }

    } catch (error) {
        Swal.close();
        Swal.fire("Error", "Tidak dapat terhubung ke server.", "error");
    } finally {
        if (btn) {
            btn.disabled = false;
        }
    }
}

async function hapusAgenda(id) {
    const konfirmasi = await Swal.fire({
        title: "Hapus Agenda?",
        text: "Data yang dihapus tidak dapat dikembalikan.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Ya",
        cancelButtonText: "Batal"
    });

    if (!konfirmasi.isConfirmed) {
        return;
    }

    Swal.fire({
        title: "Menghapus...",
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    try {
        const response = await fetch(`/api/agenda/${id}`, { method: "DELETE" });

        Swal.close();

        if (response.ok) {
            Swal.fire("Berhasil", "Agenda berhasil dihapus.", "success").then(() => {
                location.reload();
            });
        } else {
            let message = "Agenda gagal dihapus.";

            try {
                const result = await response.json();
                message = result.detail || message;
            } catch (_) {}

            Swal.fire("Gagal", message, "error");
        }

    } catch (error) {
        Swal.close();
        Swal.fire("Error", "Tidak dapat terhubung ke server.", "error");
    }
}