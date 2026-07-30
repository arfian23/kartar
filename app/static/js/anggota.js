let editId = null;

async function simpanAnggota() {

    const data = {
        nama: document.getElementById("nama").value,
        rt: document.getElementById("rt").value,
        no_hp: document.getElementById("no_hp").value,
        alamat: document.getElementById("alamat").value,
        status: document.getElementById("status").value
    };

    let url = "/anggota/";
    let method = "POST";

    if (editId !== null) {
        url = `/anggota/${editId}`;
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

        editId = null;

        Swal.fire({
            icon: "success",
            title: "Berhasil",
            text: "Data berhasil disimpan"
        }).then(() => {
            location.reload();
        });

    } else {

        Swal.fire({
            icon: "error",
            title: "Gagal",
            text: "Data gagal disimpan"
        });

    }

}

async function hapusAnggota(id) {

    const konfirmasi = await Swal.fire({
        title: "Hapus data?",
        text: "Data anggota akan dihapus.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Ya, Hapus",
        cancelButtonText: "Batal"
    });

    if (!konfirmasi.isConfirmed) {
        return;
    }

    const response = await fetch(`/anggota/${id}`, {
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

        Swal.fire({
            icon: "error",
            title: "Gagal",
            text: "Data gagal dihapus"
        });

    }

}

async function editAnggota(id) {

    const response = await fetch(`/anggota/${id}`);
    const data = await response.json();

    editId = id;

    document.getElementById("nama").value = data.nama;
    document.getElementById("rt").value = data.rt;
    document.getElementById("no_hp").value = data.no_hp ?? "";
    document.getElementById("alamat").value = data.alamat ?? "";
    document.getElementById("status").value = data.status;

    const modal = new bootstrap.Modal(
        document.getElementById("modalTambah")
    );

    modal.show();

}