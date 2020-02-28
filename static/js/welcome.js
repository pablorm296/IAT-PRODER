
//Función para el botón de ok
function okBtn() {
    //Registrar acción en API
    //*-*-*--*-*-*-*-
    //Ir a página de instrucciones
    window.location.href = "https://www.google.com.mx/";
}

//Función para el botón de saber más
function infoBtn() {
    //Mostrar el PopUp
    $("#PopUp").show();
}

//Función para el botón de cancelar
function noBtn() {
    //Registrar acción en API
    //*-*-*--*-*-*-*-
    //Ir a Google
    window.location.href = "https://www.google.com.mx/";
}

//Función para el botón de cerrar popup
function closePopUpBtn() {
    //Cerrar el PopUp
    $("#PopUp").hide();
}

//Función para configurar botones
function setBtns() {
    //Botón ok
    $("#OkButton").click(okBtn);
    //Botón para mayor información
    $("#infoButton").click(infoBtn);
    //Botón para cancelar
    $("#NoButton").click(noBtn);
    //Botón que cierra el PopUp
    $("#PopUpClose").click(closePopUpBtn);
    //Si el usuario da click en cualquier lugar de la ventana, cerramos el PopUp
    window.onclick = closePopUpBtn;
}

//Cuando el documento se carga
$(document).ready(function () {
    //Configuramos botones
    setBtns();
    //Inicializamos conector de API
    myAPI = new iatAPI()
    //Obtenemos nuevo usuario
    myAPI.endPoints.POST_newUser();
});