// Check if device is in portrait or landscape mode
function checkOrientation () {
    if(window.innerHeight > window.innerWidth){
        alert("Por favor, coloca tu dispositivo en posición horizontal.");
    }
}

// When document loads
$(document).ready(function () {
    // Check device orientation
    checkOrientation();
    // Bind checkOrientation as resize handler
    $(window).resize(checkOrientation);
});