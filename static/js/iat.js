var __stage = 1;
var __order;
var __trialCount;
var __stageLength;
var __trialStart;
var __imgCat = ["Piel clara", "Piel oscura"];
var __wrdCat = ["Bueno", "Malo"];
var __imgLabel = ["white", "dark"];
var __wrdLabel = ["good", "bad"]
var __instructions = false;
var __left;
var __right;
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
            myAPI.endPoints.GET_stimuli(__stage);
            __instructions = false;
        }
    } else {
        if (keyName == "space") {
            return false
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
            console.log("correcto");
            __trialCount += 1;
            playIAT();
        } else {
            console.log("incorrecto");
        }
    } else {
        if (__right.includes(currentLabel)) {
            console.log("correcto");
            __trialCount += 1;
            playIAT();
        } else {
            console.log("incorrecto");
        }
    }
}

//Función para asignar labels a las columnas
function assignLabelsAndText(stageType, inverse) {

    //Definimos variables (elementos donde guardamos el texto)
    var leftColTxt = $("#leftColTitle");
    var rightColTxt = $("#rightColTitle");
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

    //Dependiendo del tipo de bloque, llenamos distintas variables
    //Un bloque con palabras e imágenes
    if (stageType == "word&img") {
        //Asignamos los labels
        __left = [__wrdLabel[order], __imgLabel[order]];
        __right = [__wrdLabel[order + (1 * modifier)], __imgLabel[order + (1 * modifier)]];
        //Cambiamos el texto
        leftImgLabel.innerText = __imgCat[order];
        rightImgLabel.innerText = __imgCat[order + (1 * modifier)];
        leftWrdLabel.innerText = __wrdCat[order];
        rightWrdLabel.innerText = __wrdCat[order + (1 * modifier)];
        //Mostramos los campos
        leftImgLabel.style.display = "block";
        leftOr.style.display = "block";
        leftWrdLabel.style.display = "block";
        rightImgLabel.style.display = "block";
        rightOr.style.display = "block";
        rightWrdLabel.style.display = "block";

        //Un bloque con solo palabras
    } else if (stageType == "word") {
        //Asignamos los labels
        __left = [__wrdLabel[order]];
        __right = [__wrdLabel[order + (1 * modifier)]];
        //Cambiamos el texto
        leftWrdLabel.innerText = __wrdCat[order];
        rightWrdLabel.innerText = __wrdCat[order + (1 * modifier)];
        //Mostramos los campos
        leftWrdLabel.style.display = "block";
        rightWrdLabel.style.display = "block";

        //Un bloque con solo imagenes
    } else if (stageType == "img") {
        //Asignamos los labels
        __left = [__imgLabel[order]];
        __right = [__imgLabel[order + (1 * modifier)]];
        //Cambiamos el texto
        leftImgLabel.innerText = __imgCat[order];
        rightImgLabel.innerText = __imgCat[order + (1 * modifier)];
        //Mostramos los campos
        leftImgLabel.style.display = "block";
        rightImgLabel.style.display = "block";

    } else {
        throw "Invalid stageType";
    }
}

//Función para mostrar instrucciones
function showInstructions() {
    __instructions = true;
    //Colocar títulos 
    switch (__stage) {
        case 1:
            assignLabelsAndText("word", false);
            break;
        case 2:
            assignLabelsAndText("img", false);
            break;
        case 3:
            assignLabelsAndText("word&img", false);
            break;
        case 4:
            assignLabelsAndText("word&img", false);
            break;
        case 5:
            assignLabelsAndText("word", true);
            break;
        case 6:
            assignLabelsAndText("word&img", true);
            break;
        case 7:
            assignLabelsAndText("word&img", true);
            break;
    }
}

//Función para colocalr estímulos
function placeStimuli(stimuliArray) {
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
        console.log(holder);
        //Ocultamos el holder
        $(holder).hide();
        //Imagen o palabra?
        if (stimuliType == "img") {
            // Contenido del estímulo
            $(holder).html(`<img src='../imgs/stimuli/${stimuliContent}.jpg'>`);
            // Categoría del estímulo
            $(holder).attr("label", stimuliLabel);
        } else {
            // Contenido del estímulo
            $(holder).html(stimuliContent);
            // Categoría del estímulo
            $(holder).attr("label", stimuliLabel);
        }
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
        //Salir
    } else if (__stage == 1) {
        //Determinar orden
        __order = randomInt(0, 1);
    }

    //Cambiamos el texto indicando en qué ronda nos encontramos
    $("#rndCount").text(`Ronda ${__stage} de 7`);

    //Cargamos instrucciones
    showInstructions();
}

//Cuando el documento se carga
$(document).ready(function () {
    IATloop();
    $(document).keypress(function (e) {
        e.preventDefault();
        keyHandler(e, true, keyCallBack);
    });
});