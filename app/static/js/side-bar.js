const hamBurger = document.querySelector(".toggle-btn");
hamBurger.addEventListener("click", function () {
    document.querySelector("#sidebar").classList.toggle("expand");
});
function imageCliquable() {
    const hamBurger = document.querySelector(".toggle-btn");
    hamBurger.addEventListener("click", function () {
        document.querySelector("#sidebar").classList.toggle("expand");
        var div = document.getElementById("monDiv");
        div.innerHTML = "<button class=\"toggle-btn\" type=\"button\" ><i class=\"lni lni-grid-alt\"></i></button>";

    });
}

function changerContenu() {
    var div = document.getElementById("monDiv");
    div.innerHTML = "<button class=\"toggle-btn\" type=\"button\"><div class=\"sidebar-logo\"><a href=\"\" class=\"logo-container\"><img  src=\"{% static 'img/Greenlogo.png' %}\" alt=\"Green Logo\" onclick=\"imageCliquable()\"></a></div> </button>";
}
