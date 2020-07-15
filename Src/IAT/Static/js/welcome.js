
// Ok button function
function okBtn() {
    // Go to instructions page
    window.location.href = "/instructions";
}

// More info button
function infoBtn() {
    // Show PopUp and go to top
    $("#PopUp").show();
    $('html, body').animate({ scrollTop: 0}, 'fast');
}

// Cancel button
function noBtn() {
    // Go to project page
    window.location.href = "https://discriminacion.colmex.mx/";
}

// Close PopUp button
function closePopUpBtn() {
    $("#PopUp").hide();
}

// Set Buttons actions
function setBtns() {
    $("#OkButton").click(okBtn);
    $("#InfoButton").click(infoBtn);
    $("#NoButton").click(noBtn);
    $("#PopUpClose").click(closePopUpBtn);
    // When click outside the PopUp, close it
    $("#PopUp").click(closePopUpBtn).children().click(function (e) {
        return false;
    })
}

// When document loads, set buttons action
$(document).ready(function () {
    setBtns();
});