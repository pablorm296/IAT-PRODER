
//Función para el botón de ok
function okBtn() {

}

//Función para el botón de saber más
function infoBtn() {

}

//Función para el botón de cancelar
function noBtn() {
    //Registrar acción en API
    //*-*-*--*-*-*-*-
    //Ir a Google
    window.location.href = "https://www.google.com.mx/";
}

//Función para configurar botones
function setBtns() {
    //Botón ok
    $("#OkButton").click(okBtn());
    //Botón para mayor información
    $("#infoButton").click(infoBtn());
    //Botón para cancelar
    $("#NoButton").click(noBtn());
}

//Cuando el documento se carga
$(document).ready(function () {
    setBtns();
});