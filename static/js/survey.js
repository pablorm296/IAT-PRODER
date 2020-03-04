
//Función para el botón de ok
function okBtn() {
    //Registrar acción en API
    myAPI.endPoints.GET_results();
    //Ir a página de instrucciones
}

//Función para configurar botones
function setBtns() {
    //Botón ok
    $("#OkButton").click(okBtn);
    //Botón para mayor información
}

//Cuando el documento se carga
$(document).ready(function () {
    //Configuramos botones
    setBtns();
    //Inicializamos conector de API
    myAPI = new iatAPI()
});