// static/js/main.js

document.addEventListener("DOMContentLoaded", function () {
    let navLinks = document.querySelectorAll(".nav-link");

    navLinks.forEach(function (link) {
        link.addEventListener("mouseenter", function () {
            this.style.backgroundColor = "black";
            this.style.color = "white";
            this.style.borderRadius = "5px"; // optional for rounded effect
        });

        link.addEventListener("mouseleave", function () {
            this.style.backgroundColor = "";
            this.style.color = "";
        });
    });
});
