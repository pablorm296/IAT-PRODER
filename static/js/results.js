var __iatScore;

//Función para el botón de ok
function okBtn() {
    
}

//Función para poner resultados
function loadResults() {
    myAPI.endPoints.GET_results(function (data) {
        //Seleccionar objeto de interés
        const responseContent = data.responseContent;
        //Extraemos variables de interés
        const iatScore = responseContent.iatScore;
        const fastestLatency = responseContent.fastestLatency;
        const slowestLatency = responseContent.slowestLatency;
        const meanLatency = responseContent.meanLatency;
        const errorCount = responseContent.errorCount;
        //Colocamos los resiltados en la página
        __iatScore = iatScore;
        $("#result_iat_score").text(iatScore);
    });
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
    myAPI = new iatAPI();
    //Cargamos resultados
    loadResults();
});