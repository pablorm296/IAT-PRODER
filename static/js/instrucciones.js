const __stage = 0;
var myAPI;

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

//Función callback para las teclas
function keyCallBack(keyName) {
    if (keyName == "space") {
        window.location.href = "/IAT/static/src/iat.php";
    }
}

//Colocar ejemplos
function putExamples(data) {
    //Obtener catgeorías de ejemplos
    const goodWords = data.good;
    const badWords = data.bad;
    const whitePeople = data.white;
    const darkPeope = data.dark;
    //Ponemos los ejemplos
    //Palabras buenas
    for (let index = 0; index < goodWords.length; index++) {
        //Obtenemos la palabra
        const word = goodWords[index];
        //La agregamos a la lista de palabras
        $("#good_examples").append(word);
        //Si no es la última palabra
        if (index < goodWords.length - 1) {
            $("#good_examples").append(",");
        }
    }
    //Palabras malas
    for (let index = 0; index < badWords.length; index++) {
        //Obtenemos la palabra
        const word = badWords[index];
        //La agregamos a la lista de palabras
        $("#good_examples").append(word);
        //Si no es la última palabra
        if (index < badWords.length - 1) {
            $("#good_examples").append(",");
        }
    }
}

//Cuando el documento se carga
$(document).ready(function () {
    //Asignamos handler y key de las teclas
    $(document).keypress(function (e) {
        e.preventDefault();
        keyHandler(e, false, keyCallBack);
    });
    //Lllamamos los estímulos necesarios
    //Nueva instancia de myAPI
    myAPI = new iatAPI()
    myAPI.endPoints.GET_stimuli(__stage, putExamples);
});