// More info button
function infoBtn() {
    // Go to project page
    window.location.href = "https://discriminacion.colmex.mx/";
}

// Set Buttons actions
function setBtns() {
    $("#InfoButton").click(infoBtn);
}

// When document loads, set buttons action
$(document).ready(function () {
    setBtns();
});