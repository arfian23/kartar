const modalUser = new bootstrap.Modal(document.getElementById("modalUser"));

let mode = "create";

let currentId = null;


// ===============================
// LOAD ANGGOTA
// ===============================
async function loadAnggota() {

    try {

        const response = await fetch("/api/users/anggota/list");

        const data = await response.json();

        const select = document.getElementById("anggota_id");

        select.innerHTML = `
            <option value="">
                -- Pilih Anggota --
            </option>
        `;

        data.forEach(item => {

            select.innerHTML += `
                <option value="${item.id}">
                    ${item.nama}
                </option>
            `;

        });

    }

    catch (err) {

        console.error(err);

        Swal.fire(
            "Error",
            "Gagal mengambil data anggota.",
            "error"
        );

    }

}


// ===============================
// RESET FORM
// ===============================
function resetForm() {

    currentId = null;

    mode = "create";

    document.getElementById("modalTitle").innerHTML = "Tambah User";

    document.getElementById("formUser").reset();

    document.getElementById("userId").value = "";

    document.getElementById("status").value = "true";

    document.getElementById("anggota_id").value = "";

}


// ===============================
// TOMBOL TAMBAH USER
// ===============================
document
.getElementById("btnTambahUser")
.addEventListener("click", async function () {

    resetForm();

    await loadAnggota();

    modalUser.show();

});


// ===============================
// LOAD SAAT HALAMAN DIBUKA
// ===============================
document.addEventListener("DOMContentLoaded", async () => {

    await loadAnggota();

});

// ===============================
// SIMPAN USER
// ===============================
document
.getElementById("btnSimpan")
.addEventListener("click", async function () {

    const username = document.getElementById("username").value.trim();

    const nama_lengkap = document.getElementById("nama_lengkap").value.trim();

    const password = document.getElementById("password").value;

    const role = document.getElementById("role").value;

    const status = document.getElementById("status").value === "true";

    const anggota = document.getElementById("anggota_id").value;

    if (username === "" || nama_lengkap === "") {

        Swal.fire(
            "Peringatan",
            "Username dan Nama Lengkap wajib diisi.",
            "warning"
        );

        return;
    }

    if (mode === "create" && password === "") {

        Swal.fire(
            "Peringatan",
            "Password wajib diisi.",
            "warning"
        );

        return;
    }

    const body = {

        username: username,

        nama_lengkap: nama_lengkap,

        password: password,

        role: role,

        status: status,

        anggota_id: anggota === "" ? null : parseInt(anggota)

    };

    try {

        let response;

        // ===============================
        // CREATE
        // ===============================
        if (mode === "create") {

            response = await fetch("/api/users/", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(body)

            });

        }

        // ===============================
        // UPDATE
        // ===============================
        else {

            if (password === "") {
                delete body.password;
            }

            response = await fetch(`/api/users/${currentId}`, {

                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(body)

            });

        }

        const result = await response.json();

        if (!response.ok) {

            Swal.fire(
                "Gagal",
                result.detail ?? "Terjadi kesalahan.",
                "error"
            );

            return;
        }

        Swal.fire({

            icon: "success",

            title: "Berhasil",

            text: mode === "create"
                ? "User berhasil ditambahkan."
                : "User berhasil diperbarui."

        }).then(() => {

            location.reload();

        });

    }

    catch (err) {

        console.error(err);

        Swal.fire(
            "Error",
            "Tidak dapat terhubung ke server.",
            "error"
        );

    }

});

// ===============================
// EDIT USER
// ===============================
document.addEventListener("click", async function (e) {

    if (!e.target.closest(".btn-edit")) return;

    const id = e.target.closest(".btn-edit").dataset.id;

    currentId = id;

    mode = "edit";

    document.getElementById("modalTitle").innerHTML = "Edit User";

    await loadAnggota();

    try {

        const response = await fetch(`/api/users/${id}`);

        const user = await response.json();

        if (!response.ok) {

            Swal.fire(
                "Error",
                user.detail ?? "User tidak ditemukan.",
                "error"
            );

            return;

        }

        document.getElementById("userId").value = user.id;

        document.getElementById("username").value = user.username;

        document.getElementById("nama_lengkap").value = user.nama_lengkap;

        document.getElementById("password").value = "";

        document.getElementById("role").value = user.role;

        document.getElementById("status").value = user.status.toString();

        if (user.anggota_id !== null) {

            document.getElementById("anggota_id").value = user.anggota_id;

        } else {

            document.getElementById("anggota_id").value = "";

        }

        modalUser.show();

    }

    catch (err) {

        console.error(err);

        Swal.fire(
            "Error",
            "Gagal mengambil data user.",
            "error"
        );

    }

});


// ===============================
// DELETE USER
// ===============================
document.addEventListener("click", async function (e) {

    if (!e.target.closest(".btn-delete")) return;

    const id = e.target.closest(".btn-delete").dataset.id;

    const konfirmasi = await Swal.fire({

        title: "Hapus User?",

        text: "Data user akan dihapus secara permanen.",

        icon: "warning",

        showCancelButton: true,

        confirmButtonText: "Ya, Hapus",

        cancelButtonText: "Batal"

    });

    if (!konfirmasi.isConfirmed) {

        return;

    }

    try {

        const response = await fetch(`/api/users/${id}`, {

            method: "DELETE"

        });

        const result = await response.json();

        if (!response.ok) {

            Swal.fire(
                "Gagal",
                result.detail ?? "Tidak dapat menghapus user.",
                "error"
            );

            return;

        }

        Swal.fire({

            icon: "success",

            title: "Berhasil",

            text: result.message

        }).then(() => {

            location.reload();

        });

    }

    catch (err) {

        console.error(err);

        Swal.fire(
            "Error",
            "Tidak dapat terhubung ke server.",
            "error"
        );

    }

});