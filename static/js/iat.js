var __stage = 1;
var __order;
var __trialCount;
var __stageLength;
var __trialStart;
var __imgCat = ["Piel clara", "Piel oscura"];
var __imgCatInstructions = ["piel clara", "piel oscura"];
var __wrdCat = ["Bueno", "Malo"];
var __wrdCatInstructions = ["palabras buenas", "palabras malas"];
var __imgLabel = ["white", "dark"];
var __wrdLabel = ["good", "bad"]
var __instructions = false;
var __left;
var __right;
var __results = {};
var __errorCnt = 0;
var myAPI;

//Función para generar un entero aleatorio
function randomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

//Función para controlar presión de teclas  
function keyHandler(e, v = false, c) {
    //Inicializamos variable para guardar código de tecla
    var keyCode;

    //IE y otros exploradores
    if (window.event) { // IE                    
        keyCode = e.keyCode;
    } else if (e.which) { // Netscape/Firefox/Opera                   
        keyCode = e.which;
    }

    //Obtenemos tecla apretada
    var keyName = String.fromCharCode(keyCode);
    //En caso de barra espaciadora
    if (keyName === " ") {
        keyName = "space";
    }
    //Enviamos a log
    if (v) {
        console.log("Key pressed:" + keyName);
    }
    //Si hay callback
    if (c) {
        c(keyName);
    } else {
        return keyName;
    }
}

//Función que procesa la acción asignada a las teclas
function keyCallBack(keyName) {
    if (__instructions) {
        if (keyName == "space") {
            $("#loader").show();
            myAPI.endPoints.GET_stimuli(__stage, placeStimuli);
            __instructions = false;
            //Ocultamos instrucciones e indicación de proceder
            if (screenfull.isFullscreen) {
                console.log("La pantalla ya está maximizada");
            } else {
                screenfull.request();
            }
            // Hide space bar indication
            $("#space_bar").hide();
            // Hide instructions 
            $("#instructions").hide();
            // Hide round count
            $("#rndCount").hide();
            // Set blank div class
            $("#blank").removeClass("blank");
            $("#blank").addClass("blank_bigger");
        }
    } else {
        if (keyName == "space") {
            return false;
        }
        if (keyName == "e") {
            iatAnswer(keyName);
        }
        if (keyName == "i") {
            iatAnswer(keyName);
        }
    }
}

//Función que se activa cuando el usuario responde un estímulo
function iatAnswer(key) {
    const humanIndex = __trialCount + 1;
    const holder = `#stimHolder_${humanIndex}`;
    const currentLabel = $(holder).attr("label");
    if (key == "e") {
        if (__left.includes(currentLabel)) {
            const ellapsed = getLatency();
            saveTrial(ellapsed);
            console.log(`correcto (${ellapsed} ms)`);
            hideText("info");
            __trialCount += 1;
            playIAT();
        } else {
            console.log("incorrecto");
            __errorCnt += 1;
            showError();
        }
    } else {
        if (__right.includes(currentLabel)) {
            const ellapsed = getLatency();
            saveTrial(ellapsed);
            console.log(`correcto (${ellapsed} ms)`);
            hideText("info");
            __trialCount += 1;
            playIAT();
        } else {
            console.log("incorrecto");
            __errorCnt += 1;
            showError();
        }
    }
}

//Función para registrar la latencia
function getLatency() {
    const Now = new Date();
    const diff = Math.abs(Now - __trialStart);
    return diff;
}

//Función para guardar los resultados
function saveTrial(latency) {
    //Obtener el stage en el que estamos (en índice 0)
    const stage = __stage - 1;
    //Obtenemos el tipo de estímulo y su contenido
    const humanIndex = __trialCount + 1;
    const holder = `#stimHolder_${humanIndex}`;
    const stimLabel = $(holder).attr("label");
    const stimType = $(holder).attr("type");
    const stimValue = $(holder).attr("val");
    const error = __errorCnt;
    //Creamos un objeto con la información del estímulo
    const stimObj = {
        latency: latency,
        type: stimType,
        label: stimLabel,
        value: stimValue,
        error: error
    };
    //Lo agregamos
    __results[`round_${__stage}`].push(stimObj);
}

//Función que se activa cuando el usuario comete un error
function showError() {
    //Elementos donde se encuentra nuestro texto
    var errorMark = $("#errorMrk");
    var errorMsg = $("#errorMsg")
    //Los mostramos
    errorMark.show();
    errorMsg.show();
}

//Función para asignar labels a las columnas
function assignLabelsAndText(stageType, msg, repetition, inverse) {

    //Definimos variables (elementos donde guardamos el texto)
    var leftColTxt = $("#leftColTxt");
    var rightColTxt = $("#rightColTxt");
    var leftImgLabel = leftColTxt.children("span")[0];
    var leftOr = leftColTxt.children("span")[1];
    var leftWrdLabel = leftColTxt.children("span")[2];
    var rightImgLabel = rightColTxt.children("span")[0];
    var rightOr = rightColTxt.children("span")[1];
    var rightWrdLabel = rightColTxt.children("span")[2];

    //Si estamos en un bloque donde volteamos el orden de las columnas
    var order = __order;
    if (inverse) {
        if (order === 0) {
            order = 1;
        } else if (order === 1) {
            order = 0;
        }
    }

    //Dependiendo del orden que se le asigno a la persona, creamos un modifcador
    const modifier = (order === 0) ? 1 : -1;
    const modifier_imgs = (__order === 0) ? 1 : -1;

    //Dependiendo del tipo de bloque, llenamos distintas variables
    //Un bloque con palabras e imágenes
    if (stageType == "word&img") {
        //Creamos texto de instrucciones
        const instructionsText = msg;
        //Asignamos los labels
        __left = [__wrdLabel[order], __imgLabel[__order]];
        __right = [__wrdLabel[order + (1 * modifier)], __imgLabel[__order + (1 * modifier_imgs)]];
        //Cambiamos el texto
        leftImgLabel.innerText = __imgCat[__order];
        rightImgLabel.innerText = __imgCat[__order + (1 * modifier_imgs)];
        leftWrdLabel.innerText = __wrdCat[order];
        rightWrdLabel.innerText = __wrdCat[order + (1 * modifier)];
        //Mostramos los campos
        leftImgLabel.style.display = "block";
        leftOr.style.display = "block";
        leftWrdLabel.style.display = "block";
        rightImgLabel.style.display = "block";
        rightOr.style.display = "block";
        rightWrdLabel.style.display = "block";
        //Cambiamos el texto de las instrucciones
        if (repetition) {
            $("#instructions").html("<span>Este bloque es igual al anterior.</span><br>");
            $("#instructions").append(instructionsText);
        } else {
            $("#instructions").html(instructionsText);
        }
        
        //Un bloque con solo palabras
    } else if (stageType == "word") {
        //Creamos texto de instrucciones
        const instructionsText = msg;
        //Asignamos los labels
        __left = [__wrdLabel[order]];
        __right = [__wrdLabel[order + (1 * modifier)]];
        //Cambiamos el texto
        leftWrdLabel.innerText = __wrdCat[order];
        rightWrdLabel.innerText = __wrdCat[order + (1 * modifier)];
        //Mostramos los campos
        leftWrdLabel.style.display = "block";
        rightWrdLabel.style.display = "block";
        //Cambiamos el texto de las instrucciones
        $("#instructions").html(instructionsText);
        //Un bloque con solo imagenes
    } else if (stageType == "img") {
        //Creamos texto de instrucciones
        const instructionsText = msg;
        //Asignamos los labels
        __left = [__imgLabel[__order]];
        __right = [__imgLabel[__order + (1 * modifier_imgs)]];
        //Cambiamos el texto
        leftImgLabel.innerText = __imgCat[__order];
        rightImgLabel.innerText = __imgCat[__order + (1 * modifier_imgs)];
        //Mostramos los campos
        leftImgLabel.style.display = "block";
        rightImgLabel.style.display = "block";
        //Cambiamos el texto de las instrucciones
        $("#instructions").html(instructionsText);
    } else {
        throw "Invalid stageType";
    }
}

//Función para ocultar todo el texto de la página
function hideText(which) {
    //Definimos variables (elementos donde guardamos el texto)
    //Texto de las columnas
    var leftColTxt = $("#leftColTxt");
    var rightColTxt = $("#rightColTxt");
    var leftImgLabel = leftColTxt.children("span")[0];
    var leftOr = leftColTxt.children("span")[1];
    var leftWrdLabel = leftColTxt.children("span")[2];
    var rightImgLabel = rightColTxt.children("span")[0];
    var rightOr = rightColTxt.children("span")[1];
    var rightWrdLabel = rightColTxt.children("span")[2];
    //Texto en el centro
    var roundCounter = $("#rndCount");
    var errorMark = $("#errorMrk");
    var errorMsg = $("#errorMsg")

    //Ocultamos el texto dependiendo de lo que nos pidio el usuario
    switch (which) {

        case "columns":
            leftImgLabel.style.display = "none";
            rightImgLabel.style.display = "none";
            leftOr.style.display = "none";
            rightOr.style.display = "none";
            leftWrdLabel.style.display = "none";
            rightWrdLabel.style.display = "none";

            break;

        case "info":
            roundCounter.hide();
            errorMark.hide();
            errorMsg.hide();
            break;
    }

}

//Función para mostrar instrucciones
function showInstructions() {
    __instructions = true;
    //Colocar instrucción de barra espaciadora
    $("#space_bar").text("Presiona la barra espaciadora para comenzar");
    //Colocar títulos 
    switch (__stage) {
        case 1:
            assignLabelsAndText("img", "<h1>Instrucciones:</h1><ul><li>Coloca tus dedos índices en las letras E y I de tu teclado.</li><li>Observa las palabras que aparecen en la parte superior de la pantalla, REPRESENTAN a las categorías que tendrás que ordenar. Las palabras o imágenes que tienes que ordenar aparecerán una por una en el centro de la pantalla.</li><li>Tu tarea será presionar la tecla E cuando la imagen o palabra pertenezca a la categoría del lado izquierdo. Cuando la palabra o la imagen pertenezca a la categoría de la derecha, presiona la tecla I.</li><li> Ojo: las imágenes o palabras sólo pertenecen a una categoría. Si cometes un error, aparecerá una X, para corregir el error presiona la tecla correcta tan rápido como puedas.</li><ul>", false);
            break;
        case 2:
            assignLabelsAndText("word", "<p>En este bloque tendrás que categorizar palabras. Sin embargo, las reglas son las mismas</p><b>Palabras buenas:</b> competente, trabajador, constante, cariñoso, tierno, amoroso, dulce<p></p><p><b>Palabras malas:</b> agresivo, rudo, problemático, violento, mediocre, conformista, mentiroso, corrupto.</p>", false);
            break;
        case 3:
            assignLabelsAndText("word&img", "<p>En esta sección tendrás que ordenar imágenes y palabras.</p><p>Las etiquetas verdes corresponden a las palabras y las blancas a las imágenes.</p>", false, false);
            break;
        case 4:
            assignLabelsAndText("word&img", "<p>Ordena las mismas dos categorías de nuevo.</p>", false, false);
            break;
        case 5:
            assignLabelsAndText("img", "<p>Aviso, ahora sólo hay dos categorías y han cambiado de posición. Practica en esta nueva configuración.</p>", true);
            break;
        case 6:
            assignLabelsAndText("word&img", "<p>Observa la parte de arriba, ahora aparecen categorías dobles nuevamente.</p><p>Usa las teclas E y I para ordenar los elementos.</p>", false, true);
            break;
        case 7:
            assignLabelsAndText("word&img", "<p>Ordena las mismas categorías de nuevo.</p>", false, true);
            break;
    }
    //Mostrar contador de rondas, instrucciones e indicación de proceder
    $("#space_bar").show();
    $("#instructions").show();
    $("#rndCount").show();
    //Definir tamaño del placeholder
    // Set blank div class
    $("#blank").removeClass("blank_bigger");
    $("#blank").addClass("blank");
}

//Función para colocalr estímulos
function placeStimuli(data) {
    const stimuliArray = data.responseContent;
    //Guardar tamaño de prueba
    __stageLength = stimuliArray.length;
    //Colocar estímulos
    for (let i = 0; i < stimuliArray.length; i++) {
        const humanIndex = i + 1;
        const holder = `#stimHolder_${humanIndex}`;
        const stimuli = stimuliArray[i];
        const stimuliType = stimuli.type;
        const stimuliLabel = stimuli.label;
        const stimuliContent = stimuli.content;
        //Ocultamos el holder
        $(holder).removeClass("wrd");
        $(holder).hide();
        //Imagen o palabra?
        if (stimuliType == "img") {
            // Contenido del estímulo
            $(holder).html(`<img src='../imgs/stimuli/${stimuliContent}.jpg'>`);
        } else {
            // Contenido del estímulo
            $(holder).html(stimuliContent);
            $(holder).addClass("wrd");
        }
        // Agregamos información del estímulo (categoría, tipo y contenido)
        $(holder).attr("label", stimuliLabel);
        $(holder).attr("type", stimuliType);
        $(holder).attr("val", stimuliContent);
        //Cuando las imágenes ya se cargaron
        $('.stimuli').imagesLoaded(function () {
            //Ocultar el spiner
            $("#loader").hide();
            //Ir a función que muestra estímulos
            __trialCount = 0;
            playIAT();
        });
    }
}

//Función para jugar al IAT
function playIAT() {
    const humanIndex = __trialCount + 1;
    //Cuántos estímulos hay? Si ya hicimos más, salir al siguiente bloque
    if (__trialCount < __stageLength) {
        //Si no es el primero, ocultar último holder en aparecer
        if (__trialCount != 0) {
            $(`#stimHolder_${humanIndex - 1}`).hide();
        }
        //Mostrar estímulo
        $(`#stimHolder_${humanIndex}`).show();
        //Iniciar conteo
        __trialStart = new Date();
        //Reiniciar cuenta de errores
        __errorCnt = 0;
    } else {
        $(`#stimHolder_${humanIndex - 1}`).hide();
        __stage += 1;
        IATloop();
    }
}

//Función principal del IAT
function IATloop() {
    $("#loader").hide();
    // Verificar en qué stage estamos
    if (__stage > 7) {
        //Creamos un objeto con los resultados finales
        const finalResults = {
            results: __results,
            order: __order
        }

        //Enviamos los resultados al servidor
        myAPI.endPoints.POST_results(finalResults);
        //Vamos a la página de la encuesta
        window.location.href = "/IAT/static/src/survey.php";

        //Salir a la encuesta
    } else if (__stage == 1) {
        //Determinar orden
        __order = randomInt(0, 1);
    }

    // Guardar el stage en el objeto de resultados
    var stageObj = [];
    __results[`round_${__stage}`] = stageObj;

    //Cambiamos el texto indicando en qué ronda nos encontramos
    $("#rndCount").text(`Ronda ${__stage} de 7`);
    //Ocultamos el texto de las columnas
    hideText("columns");
    //Ocultamos el texto de información
    hideText("info")
    //Cargamos instrucciones
    showInstructions();
}

//Cuando el documento se carga
$(document).ready(function () {
    //Verificar ancho y alto de la página
    const w  = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    const h = window.innerHeight|| document.documentElement.clientHeight|| document.body.clientHeight;
    const min_h = 460;
    const min_w = 1000;

    if (w < min_w || h < min_h) {
        alert("La resolución de tu dispositivo es muy pequeña para realizar esta prueba. Por favor, trata de hacer más grande la pantalla o ajusta la resolución y recarga la página");
    }
    //Ir al inicio de la página
    $('html,body').scrollTop(0);
    //Iniciar IAT
    IATloop();
    //Desactivar acciones por default en teclas y asignar el keyHandler
    $(document).keypress(function (e) {
        e.preventDefault();
        keyHandler(e, false, keyCallBack);
    });
});
