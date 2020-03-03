
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
    if (keyName == "space") {
        window.location.href = "/IAT/static/src/iat.php";
    }
}

//Cuando el documento se carga
$(document).ready(function () {
    $(document).keypress(function (e) {
        e.preventDefault();
        keyHandler(e, false, keyCallBack);
    }); 
});