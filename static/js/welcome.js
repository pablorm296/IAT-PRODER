
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
    $("#OkButton").on("click", okBtn());
    //Botón para mayor información
    $("#infoButton").on("click", infoBtn());
    //Botón para cancelar
    $("#NoButton").on("click", noBtn());
}

//Cuando el documento se carga
$(document).ready(function () {
    //Configuramos botones
    setBtns();
    //Inicializamos conector de API
    myAPI = new iatAPI()
});