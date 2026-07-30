// ==========================================================
// Layout Script - Karang Taruna Sendangan
// Handle toggle sidebar (desktop & mobile) + auto reset saat resize
// ==========================================================

document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("sidebar");
    const content = document.getElementById("content");
    const toggle = document.getElementById("toggleSidebar");

    toggle.addEventListener("click", function () {

        if (window.innerWidth <= 768) {

            // Mode mobile: sidebar muncul sebagai overlay
            sidebar.classList.toggle("show");

        } else {

            // Mode desktop: sidebar collapse & content menyesuaikan
            sidebar.classList.toggle("hide");
            content.classList.toggle("full");

        }

    });

    // Reset state sidebar saat window di-resize
    // (biar tidak ada state "nyangkut" ketika pindah dari mobile <-> desktop)
    window.addEventListener("resize", function () {

        if (window.innerWidth > 768) {

            sidebar.classList.remove("show");

        } else {

            sidebar.classList.remove("hide");
            content.classList.remove("full");

        }

    });

});