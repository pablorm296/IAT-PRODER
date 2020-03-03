var __stage = 1;
var __order;
var __trialCount;
var __stageLength;
var __trialStart;
var __imgCat = ["Piel clara", "Piel oscura"];
var __wrdCart = ["Bueno", "Malo"];
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

//Función para mostrar instrucciones
function showInstructions() {
    __instructions = true;
    //Colocar títulos 
    switch (__stage) {
        case 1:
            if (__order == 1) {
                __left = [__wrdLabel[__order]];
                __right = [__wrdLabel[__order - 1]];
                $("#leftColTitle").children("span")[0].innerText = __wrdCart[__order];
                $("#rightColTitle").children("span")[0].innerText = __wrdCart[__order - 1];

                $("#leftColTitle").children("span")[0].style.display = "block";
                $("#rightColTitle").children("span")[0].style.display = "block";
                $("#leftColTitle").children("span")[1].style.display = "none";
                $("#rightColTitle").children("span")[1].style.display = "none";
                $("#leftColTitle").children("span")[2].style.display = "none";
                $("#rightColTitle").children("span")[2].style.display = "none";
            } else {
                __left = [__wrdLabel[__order]];
                __right = [__wrdLabel[__order + 1]];
                $("#leftColTitle").children("span")[0].innerText = __wrdCart[__order];
                $("#rightColTitle").children("span")[0].innerText = __wrdCart[__order + 1];

                $("#leftColTitle").children("span")[0].style.display = "block";
                $("#rightColTitle").children("span")[0].style.display = "block";
                $("#leftColTitle").children("span")[1].style.display = "none";
                $("#rightColTitle").children("span")[1].style.display = "none";
                $("#leftColTitle").children("span")[2].style.display = "none";
                $("#rightColTitle").children("span")[2].style.display = "none";
            }
            break;
        case 2:
            if (__order == 1) {
                __left = [__imgLabel[__order]];
                __right = [__imgLabel[__order - 1]];
                $("#leftColTitle").children("span")[0].innerText = __imgCat[__order];
                $("#rightColTitle").children("span")[0].innerText = __imgCat[__order - 1];

                $("#leftColTitle").children("span")[0].style.display = "block";
                $("#rightColTitle").children("span")[0].style.display = "block";
                $("#leftColTitle").children("span")[1].style.display = "none";
                $("#rightColTitle").children("span")[1].style.display = "none";
                $("#leftColTitle").children("span")[2].style.display = "none";
                $("#rightColTitle").children("span")[2].style.display = "none";
            } else {
                __left = [__imgLabel[__order]];
                __right = [__imgLabel[__order + 1]];
                $("#leftColTitle").children("span")[0].innerText = __imgCat[__order];
                $("#rightColTitle").children("span")[0].innerText = __imgCat[__order + 1];

                $("#leftColTitle").children("span")[0].style.display = "block";
                $("#rightColTitle").children("span")[0].style.display = "block";
                $("#leftColTitle").children("span")[1].style.display = "none";
                $("#rightColTitle").children("span")[1].style.display = "none";
                $("#leftColTitle").children("span")[2].style.display = "none";
                $("#rightColTitle").children("span")[2].style.display = "none";
            }
            break;
        case 3:
            if (__order == 1) {
                __left = [__imgLabel[__order], __wrdLabel[__order]];
                __right = [__imgLabel[__order - 1], __wrdLabel[__order - 1]];
                $("#leftColTitle").children("span")[0].innerText = __imgCat[__order];
                $("#rightColTitle").children("span")[0].innerText = __imgCat[__order - 1];
                $("#leftColTitle").children("span")[2].innerText = __wrdCart[__order];
                $("#rightColTitle").children("span")[2].innerText = __wrdCart[__order - 1];

                $("#leftColTitle").children("span")[0].style.display = "block";
                $("#rightColTitle").children("span")[0].style.display = "block";
                $("#leftColTitle").children("span")[1].style.display = "block";
                $("#rightColTitle").children("span")[1].style.display = "block";
                $("#leftColTitle").children("span")[2].style.display = "block";
                $("#rightColTitle").children("span")[2].style.display = "block";
            } else {
                __left = [__imgLabel[__order], __wrdLabel[__order]];
                __right = [__imgLabel[__order - 1], __wrdLabel[__order + 1]];
                $("#leftColTitle").children("span")[0].innerText = __imgCat[__order];
                $("#rightColTitle").children("span")[0].innerText = __imgCat[__order + 1];
                $("#leftColTitle").children("span")[2].innerText = __wrdCart[__order];
                $("#rightColTitle").children("span")[2].innerText = __wrdCart[__order + 1];

                $("#leftColTitle").children("span")[0].style.display = "block";
                $("#rightColTitle").children("span")[0].style.display = "block";
                $("#leftColTitle").children("span")[1].style.display = "block";
                $("#rightColTitle").children("span")[1].style.display = "block";
                $("#leftColTitle").children("span")[2].style.display = "block";
                $("#rightColTitle").children("span")[2].style.display = "block";
            }
            break;
        case 4:
            if (__order == 1) {
                __left = [__imgLabel[__order], __wrdLabel[__order]];
                __right = [__imgLabel[__order - 1], __wrdLabel[__order - 1]];
                $("#leftColTitle").children("span")[0].innerText = __imgCat[__order];
                $("#rightColTitle").children("span")[0].innerText = __imgCat[__order - 1];
                $("#leftColTitle").children("span")[2].innerText = __wrdCart[__order];
                $("#rightColTitle").children("span")[2].innerText = __wrdCart[__order - 1];

                $("#leftColTitle").children("span")[0].style.display = "block";
                $("#rightColTitle").children("span")[0].style.display = "block";
                $("#leftColTitle").children("span")[1].style.display = "block";
                $("#rightColTitle").children("span")[1].style.display = "block";
                $("#leftColTitle").children("span")[2].style.display = "block";
                $("#rightColTitle").children("span")[2].style.display = "block";
            } else {
                __left = [__imgLabel[__order], __wrdLabel[__order]];
                __right = [__imgLabel[__order - 1], __wrdLabel[__order + 1]];
                $("#leftColTitle").children("span")[0].innerText = __imgCat[__order];
                $("#rightColTitle").children("span")[0].innerText = __imgCat[__order + 1];
                $("#leftColTitle").children("span")[2].innerText = __wrdCart[__order];
                $("#rightColTitle").children("span")[2].innerText = __wrdCart[__order + 1];

                $("#leftColTitle").children("span")[0].style.display = "block";
                $("#rightColTitle").children("span")[0].style.display = "block";
                $("#leftColTitle").children("span")[1].style.display = "block";
                $("#rightColTitle").children("span")[1].style.display = "block";
                $("#leftColTitle").children("span")[2].style.display = "block";
                $("#rightColTitle").children("span")[2].style.display = "block";
            }
            break;
        case 5:
            if (__order == 1) {
                __right = [__wrdLabel[__order]];
                __left = [__wrdLabel[__order - 1]];
                $("#rightColTitle").children("span")[0].innerText = __wrdCart[__order];
                $("#leftColTitle").children("span")[0].innerText = __wrdCart[__order - 1];

                $("#rightColTitle").children("span")[0].style.display = "block";
                $("#leftColTitle").children("span")[0].style.display = "block";
                $("#rightColTitle").children("span")[1].style.display = "none";
                $("#leftColTitle").children("span")[1].style.display = "none";
                $("#rightColTitle").children("span")[2].style.display = "none";
                $("#leftColTitle").children("span")[2].style.display = "none";
            } else {
                __right = [__wrdLabel[__order]];
                __left = [__wrdLabel[__order + 1]];
                $("#rightColTitle").children("span")[0].innerText = __wrdCart[__order];
                $("#leftColTitle").children("span")[0].innerText = __wrdCart[__order + 1];

                $("#rightColTitle").children("span")[0].style.display = "block";
                $("#leftColTitle").children("span")[0].style.display = "block";
                $("#rightColTitle").children("span")[1].style.display = "none";
                $("#leftColTitle").children("span")[1].style.display = "none";
                $("#rightColTitle").children("span")[2].style.display = "none";
                $("#leftColTitle").children("span")[2].style.display = "none";
            }
            break;
        case 6:
            if (__order == 1) {
                __right = [__imgLabel[__order], __wrdLabel[__order]];
                __left = [__imgLabel[__order - 1], __wrdLabel[__order - 1]];
                $("#rightColTitle").children("span")[0].innerText = __imgCat[__order];
                $("#leftColTitle").children("span")[0].innerText = __imgCat[__order - 1];
                $("#rightColTitle").children("span")[2].innerText = __wrdCart[__order];
                $("#leftColTitle").children("span")[2].innerText = __wrdCart[__order - 1];

                $("#rightColTitle").children("span")[0].style.display = "block";
                $("#leftColTitle").children("span")[0].style.display = "block";
                $("#rightColTitle").children("span")[1].style.display = "block";
                $("#leftColTitle").children("span")[1].style.display = "block";
                $("#rightColTitle").children("span")[2].style.display = "block";
                $("#leftColTitle").children("span")[2].style.display = "block";
            } else {
                __right = [__imgLabel[__order], __wrdLabel[__order]];
                __left = [__imgLabel[__order - 1], __wrdLabel[__order + 1]];
                $("#rightColTitle").children("span")[0].innerText = __imgCat[__order];
                $("#leftColTitle").children("span")[0].innerText = __imgCat[__order + 1];
                $("#rightColTitle").children("span")[2].innerText = __wrdCart[__order];
                $("#leftColTitle").children("span")[2].innerText = __wrdCart[__order + 1];

                $("#rightColTitle").children("span")[0].style.display = "block";
                $("#leftColTitle").children("span")[0].style.display = "block";
                $("#rightColTitle").children("span")[1].style.display = "block";
                $("#leftColTitle").children("span")[1].style.display = "block";
                $("#rightColTitle").children("span")[2].style.display = "block";
                $("#leftColTitle").children("span")[2].style.display = "block";
            }
            break;
        case 7:
            if (__order == 1) {
                __right = [__imgLabel[__order], __wrdLabel[__order]];
                __left = [__imgLabel[__order - 1], __wrdLabel[__order - 1]];
                $("#rightColTitle").children("span")[0].innerText = __imgCat[__order];
                $("#leftColTitle").children("span")[0].innerText = __imgCat[__order - 1];
                $("#rightColTitle").children("span")[2].innerText = __wrdCart[__order];
                $("#leftColTitle").children("span")[2].innerText = __wrdCart[__order - 1];

                $("#rightColTitle").children("span")[0].style.display = "block";
                $("#leftColTitle").children("span")[0].style.display = "block";
                $("#rightColTitle").children("span")[1].style.display = "block";
                $("#leftColTitle").children("span")[1].style.display = "block";
                $("#rightColTitle").children("span")[2].style.display = "block";
                $("#leftColTitle").children("span")[2].style.display = "block";
            } else {
                __right = [__imgLabel[__order], __wrdLabel[__order]];
                __left = [__imgLabel[__order - 1], __wrdLabel[__order + 1]];
                $("#rightColTitle").children("span")[0].innerText = __imgCat[__order];
                $("#leftColTitle").children("span")[0].innerText = __imgCat[__order + 1];
                $("#rightColTitle").children("span")[2].innerText = __wrdCart[__order];
                $("#leftColTitle").children("span")[2].innerText = __wrdCart[__order + 1];

                $("#rightColTitle").children("span")[0].style.display = "block";
                $("#leftColTitle").children("span")[0].style.display = "block";
                $("#rightColTitle").children("span")[1].style.display = "block";
                $("#leftColTitle").children("span")[1].style.display = "block";
                $("#rightColTitle").children("span")[2].style.display = "block";
                $("#leftColTitle").children("span")[2].style.display = "block";
            }
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