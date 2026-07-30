console.log("KAS_MASUK_JS LOADED");

const API_URL = "/kas_masuk";

const inputCari = document.getElementById("searchAnggota");
const hasilCari = document.getElementById("hasilAnggota");

const cardAnggota = document.getElementById("anggotaTerpilih");
const namaTerpilih = document.getElementById("namaTerpilih");
const rtTerpilih = document.getElementById("rtTerpilih");
const clearAnggota = document.getElementById("clearAnggota");


// ==============================
// SIMPAN DATA
// ==============================

async function simpanKasMasuk() {

    const kasId = document.getElementById("kas_id").value;

    const tanggalInput = document.getElementById("tanggal").value;

    const tanggalObj = new Date(tanggalInput);

    const namaBulan = [
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
    ];

    const data = {

        anggota_id: parseInt(
            document.getElementById("anggota_id").value
        ),

        tanggal: tanggalInput,

        bulan: namaBulan[tanggalObj.getMonth()],

        tahun: tanggalObj.getFullYear(),

        nominal: parseInt(
            document.getElementById("nominal").value
        ),

        metode: document.getElementById("metode").value,

        keterangan: document.getElementById("keterangan").value

    };

    if (

        !data.anggota_id ||

        !data.tanggal ||

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

    const response = await fetch(

        url,

        {

            method: method,

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(data)

        }

    );

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


// ==============================
// EDIT DATA
// ==============================

async function editKasMasuk(id) {

    const response = await fetch(

        API_URL + "/" + id

    );

    const data = await response.json();

    document.getElementById("kas_id").value = data.id;

    document.getElementById("anggota_id").value = data.anggota_id;

    if (data.anggota) {

        document.getElementById("searchAnggota").value =
            data.anggota.nama;

        namaTerpilih.innerText =
            data.anggota.nama;

        rtTerpilih.innerText =
            "RT " + data.anggota.rt;

        cardAnggota.classList.remove("d-none");

    }

    document.getElementById("tanggal").value =
        data.tanggal;

    document.getElementById("nominal").value =
        data.nominal;

    document.getElementById("metode").value =
        data.metode;

    document.getElementById("keterangan").value =
        data.keterangan;

    const modal = new bootstrap.Modal(

        document.getElementById("modalKasMasuk")

    );

    modal.show();

}

// ==============================
// HAPUS DATA
// ==============================

async function hapusKasMasuk(id) {

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

    const response = await fetch(

        API_URL + "/" + id,

        {
            method: "DELETE"
        }

    );

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


// ==============================
// AUTOCOMPLETE ANGGOTA
// ==============================

if (inputCari) {

    inputCari.addEventListener("keyup", async function () {

        const keyword = this.value.trim();

        if (keyword.length < 2) {

            hasilCari.innerHTML = "";

            return;

        }

        const response = await fetch(

            "/anggota/search?q=" +
            encodeURIComponent(keyword)

        );

        const data = await response.json();

        hasilCari.innerHTML = "";

        data.forEach(function (item) {

            hasilCari.innerHTML += `

            <button
                type="button"
                class="list-group-item list-group-item-action pilih-anggota"
                data-id="${item.id}"
                data-nama="${item.nama}"
                data-rt="${item.rt}">

                <strong>${item.nama}</strong>

                <br>

                <small>RT ${item.rt}</small>

            </button>

            `;

        });

    });

}


// ==============================
// PILIH ANGGOTA
// ==============================

document.addEventListener("click", function (e) {

    if (e.target.closest(".pilih-anggota")) {

        const btn = e.target.closest(".pilih-anggota");

        document.getElementById("anggota_id").value =
            btn.dataset.id;

        inputCari.value =
            btn.dataset.nama;

        if (namaTerpilih) {

            namaTerpilih.innerText =
                btn.dataset.nama;

        }

        if (rtTerpilih) {

            rtTerpilih.innerText =
                "RT " + btn.dataset.rt;

        }

        if (cardAnggota) {

            cardAnggota.classList.remove("d-none");

        }

        hasilCari.innerHTML = "";

        inputCari.blur();

    }

});


// ==============================
// CLEAR ANGGOTA
// ==============================

if (clearAnggota) {

    clearAnggota.addEventListener("click", function () {

        document.getElementById("anggota_id").value = "";

        inputCari.value = "";

        hasilCari.innerHTML = "";

        if (cardAnggota) {

            cardAnggota.classList.add("d-none");

        }

        inputCari.focus();

    });

}


// ==============================
// MODAL
// ==============================

const modalKas = document.getElementById("modalKasMasuk");

if (modalKas) {

    modalKas.addEventListener("shown.bs.modal", function () {

        if (document.getElementById("kas_id").value !== "") {

            return;

        }

        const today = new Date();

        document.getElementById("tanggal").value =
            today.toISOString().split("T")[0];

        document.getElementById("nominal").value = 3000;

        document.getElementById("metode").value = "Cash";

        document.getElementById("keterangan").value =
            "Kas Bulanan";

    });

    modalKas.addEventListener("hidden.bs.modal", function () {

        document.getElementById("kas_id").value = "";

        document.getElementById("anggota_id").value = "";

        inputCari.value = "";

        document.getElementById("tanggal").value = "";

        document.getElementById("nominal").value = "";

        document.getElementById("metode").value = "Cash";

        document.getElementById("keterangan").value = "";

        hasilCari.innerHTML = "";

        if (cardAnggota) {

            cardAnggota.classList.add("d-none");

        }

    });

}