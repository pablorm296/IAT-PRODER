var __iatScore;
var __histDScore;

//Función para obtener bins de los datos
//Fuente: 
function binData(data) {

    var hData = new Array(), //the output array
        size = data.length, //how many data points
        bins = Math.round(Math.sqrt(size)); //determine how many bins we need
    bins = bins > 50 ? 50 : bins; //adjust if more than 50 cells
    var max = Math.max.apply(null, data), //lowest data value
        min = Math.min.apply(null, data), //highest data value
        range = max - min, //total range of the data
        width = range / bins, //size of the bins
        bin_bottom, //place holders for the bounds of each bin
        bin_top;

    //loop through the number of cells
    for (var i = 0; i < bins; i++) {

        //set the upper and lower limits of the current cell
        bin_bottom = min + (i * width);
        bin_top = bin_bottom + width;

        //check for and set the x value of the bin
        if (!hData[i]) {
            hData[i] = new Array();
            hData[i][0] = bin_bottom + (width / 2);
        }

        //loop through the data to see if it fits in this bin
        for (var j = 0; j < size; j++) {
            var x = data[j];

            //adjust if it's the first pass
            i == 0 && j == 0 ? bin_bottom -= 1 : bin_bottom = bin_bottom;

            //if it fits in the bin, add it
            if (x > bin_bottom && x <= bin_top) {
                !hData[i][1] ? hData[i][1] = 1 : hData[i][1]++;
            }
        }
    }
    $.each(hData, function (i, point) {
        if (typeof point[1] == 'undefined') {
            hData[i][1] = 0;
        }
    });
    return hData;
}

//Función para el botón de ok
function okBtn() {
    window.location.href = "/bye"
}

//Función para dibujar el histograma
function drawPlots() {
    //Dibujamos el histograma principal
    Highcharts.chart('resultHist', {
        plotOptions: {
            column: {
                pointPadding: 0,
                borderWidth: 0,
                groupPadding: 0,
                shadow: false
            }
        },
        chart: {
            type: 'column'
        },
        tooltip: {
            enabled: false
        },
        title: {
            text: '¿Cómo se compara mi resultado con el de otros participantes?',
            style: { "font-family": "KC" }
        },
        legend: {
            enabled: false
        },
        credits: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        xAxis: [{
            labels: {
                formatter: function () {
                    var change = {
                        "0": '0<br>Sin preferencia',
                        "1": '1<br>Preferencia por piel blanca',
                        "-1": '-1<br>Preferencia por piel morena'
                    };
                    var value = change[this.value];
                    return value !== 'undefined' ? value : this.value;
                }
            },
            plotLines: [{
                color: '#FF0000', // Red
                width: 2,
                zIndex: 99,
                value: __iatScore
            }],
            title: {
                text: 'Puntaje IAT'
            },
            alignTicks: true
        }],
        yAxis: [{
            title: {
                text: 'Frecuencia'
            }
        }],

        series: [{
            name: 'Distribuciónde puntajes IAT',
            data: __histDScore
        }]
    });

}

//Función para poner los resultados
function loadResults(responseContent) {

    //Extraemos variables de interés
    const iatScore = responseContent.iatScore;
    const fastestLatency = responseContent.fastestLatency;
    const slowestLatency = responseContent.slowestLatency;
    const meanLatency = responseContent.meanLatency;
    const errorCount = responseContent.errorCount;

    const fastestLatency_group = responseContent.fastestLatency_g;
    const slowestLatency_group = responseContent.slowestLatency_g;
    const meanLatency_group = responseContent.meanLatency_g;

    const series = responseContent.dScores;

    //Verificamos que no haya variables undefined
    if (responseContent == null || iatScore == null) {
        e2Handler();
    }

    //Partimos la serie de datos en bins
    const binnedSeries = binData(series);
    __histDScore = binnedSeries;

    //Colocamos los resultados en la página
    __iatScore = iatScore;
    $("#result_iat_score").text(iatScore);
    $("#stat_mean_latency").text(meanLatency + " ms");
    $("#stat_min_latency").text(fastestLatency + " ms");
    $("#stat_max_latency").text(slowestLatency + " ms");
    $("#stat_errors").text(errorCount + " errores");
    // Group statistics
    $("#stat_mean_latency_group").text(meanLatency_group + " ms");
    $("#stat_min_latency_group").text(fastestLatency_group + " ms");
    $("#stat_max_latency_group").text(slowestLatency_group + " ms");
    $("#stat_errors_group").text("-");

    //Dependiendo de la fortaleza de los resultados
    if (iatScore < 0.2 && iatScore > -0.2) {
        $("#result_preference_size").text("no tienes preferencia (sesgo)");
        $("#result_preference_target").text("las personas de piel oscura o piel clara");
    }
    if (iatScore >= 0.2) {
        $("#result_preference_size").text("tienes una ligera preferencia (sesgo)");
        $("#result_preference_target").text("las personas de piel clara");
    }
    if (iatScore <= -0.2) {
        $("#result_preference_size").text("tienes una ligera preferencia (sesgo)");
        $("#result_preference_target").text("las personas de piel morena");
    }
    if (iatScore >= 0.5) {
        $("#result_preference_size").text("tienes una moderada preferencia (sesgo)");
        $("#result_preference_target").text("las personas de piel clara");
    }
    if (iatScore >= 0.8) {
        $("#result_preference_size").text("tienes una fuerte preferencia");
        $("#result_preference_target").text("las personas de piel clara");
    }
    if (iatScore <= -0.5) {
        $("#result_preference_size").text("tienes una moderada preferencia");
        $("#result_preference_target").text("las personas de piel oscura");
    }
    if (iatScore <= -0.8) {
        $("#result_preference_size").text("tienes una fuerte preferencia");
        $("#result_preference_target").text("las personas de piel oscura");
    }

    //Dibujamos los plots
    drawPlots();
}

//Función para poner mensaje en caso de que el tiempo de respuesta sea muy corto
function e1Handler() {
    $("#main_results").html("<p>Nos fue imposible analizar tus respuestas :( Respondiste extremadamente rápido o al azar; esto dificulta el análisis estadístico que hacemos sobre los datos.</p>");
    $("#result_iat_score").text("No disponible");
    $("#stat_mean_latency").text("No disponible");
    $("#stat_min_latency").text("No disponible");
    $("#stat_max_latency").text("No disponible");
    $("#stat_errors").text("No disponible");
    $("#results_content").hide();
}

function e2Handler() {
    $("#main_results").html("<p>Nos fue imposible analizar tus respuestas :( Ocurrió un error al intentar leer las cookies. ¿Usas algún bloqueador?</p>");
    $("#result_iat_score").text("No disponible");
    $("#stat_mean_latency").text("No disponible");
    $("#stat_min_latency").text("No disponible");
    $("#stat_max_latency").text("No disponible");
    $("#stat_errors").text("No disponible");
    $("#results_content").hide();
}

//Función para obtener resultados
function getResults() {
    //Seleccionar objeto de interés
    const responseContent = __ResultsData;
    //Extraemos variables de interés
    const statusCode = __ResultsData.code;
    //Si el servidor respondió con un error
    //Error por respuestas aleatorias
    if (statusCode == "e.1") {
        e1Handler();
    } else {
        loadResults(responseContent);
    }
}

//Función para configurar botones
function setBtns() {
    //Botón ok
    $("#InfoButton").click(okBtn);
    //Botón para mayor información
}

//Cuando el documento se carga
$(document).ready(function () {
    //Configuramos botones
    setBtns();
    //Cargamos resultados
    getResults();
});