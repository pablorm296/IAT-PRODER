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
        //Colocamos los resultados en la página
        __iatScore = iatScore;
        $("#result_iat_score").text(iatScore);
        $("#stat_mean_latency").text(meanLatency);
        $("#stat_min_latency").text(fastestLatency);
        $("#stat_max_latency").text(slowestLatency);
        $("#stat_errors").text(errorCount);

        //Dependiendo de la fortaleza de los resultados
        if (iatScore <= 0.2 || iatScore >= -0.2 ) {
            $("#result_preference_size").text("no tienes preferencia alguna");
            $("#result_preference_target").text("las personas de piel oscura o piel clara");
        } else if (iatScore >= 0.5) {
            $("#result_preference_size").text("tienes una ligera preferencia");
            $("#result_preference_target").text("las personas de piel oscura");
        } else if (iatScore >= 0.8) {
            $("#result_preference_size").text("tienes una fuerte preferencia");
            $("#result_preference_target").text("las personas de piel oscura");
        } else if (iatScore <= -0.5) {
            $("#result_preference_size").text("tienes una ligera preferencia");
            $("#result_preference_target").text("las personas de piel clara");
        } else if (iatScore <= -0.8) {
            $("#result_preference_size").text("tienes una fuerte preferencia");
            $("#result_preference_target").text("las personas de piel clara");
        }
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