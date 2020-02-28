//Función para decodificar de base64
function b64DecodeUnicode(str) {
    return decodeURIComponent(atob(str).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
}

//Función para cargar mensaje
function loadMsg() {
    if ((typeof msgContent !== 'undefined') &&
        (typeof okButtonTxt !== 'undefined') &&
        (typeof noButtonTxt !== 'undefined')) {
        //Decodificamos los mensajes
        const userType_d = b64DecodeUnicode(userType);
        const msgContent_d = b64DecodeUnicode(msgContent);
        const okButtonTxt_d = b64DecodeUnicode(okButtonTxt);
        const noButtonTxt_d = b64DecodeUnicode(noButtonTxt);
        //Cambiamos el texto
        $("#message").text(msgContent_d);
        $("#OkButton").text(okButtonTxt_d);
        $("#NoButton").text(noButtonTxt_d);
        //Mostramos botones
        $("#OkButton").show();
        $("#NoButton").show();
        //Si es un anónimo
        if (userType_d === "anon") {
            //Ocultamos botones
            $("#OkButton").hide();
            $("#NoButton").hide();
        }
        //Regresamos true
        return true
    } else {
        //Cambiamos el estilo del mensaje principal
        $("#message").toggleClass("noJsMsg");
    }
}

//Función para el botón de ok (desktop)
function okBtnDesktop() {
    $.ajax({
        type: "POST",
        url: "index.php",
        data: {
            status: "ok",
            userAgent: "desktop"
        },
        dataType: "html",
        success: function () {
            window.location.href = "/IAT/static/src/welcome.php"
        },
        statusCode: {
            400: function () {
                //Cambiamos el estilo del mensaje principal
                $("#message").toggleClass("noJsMsg");
                //Cambiamos texto del mensaje principal
                $("#message").text("¡Ups! La información enviada por el servidor ha sido comprometida o corrompida. Por favor, intenta más tarde.")
                //Ocultamos botones
                $("#OkButton").hide();
                $("#NoButton").hide();
            }
        }
    });
}

//Función para el botón de cancelar (desktop)
function noBtnDesktop() {
    $.ajax({
        type: "POST",
        url: "index.php",
        data: {
            status: "cancel",
            userAgent: "desktop"
        },
        dataType: "html",
        success: function () {
            window.location.href = "/IAT/static/src/welcome_mobile.php"
        },
        statusCode: {
            400: function () {
                //Cambiamos el estilo del mensaje principal
                $("#message").toggleClass("noJsMsg");
                //Cambiamos texto del mensaje principal
                $("#message").text("¡Ups! La información enviada por el servidor ha sido comprometida o corrompida. Por favor, intenta más tarde.")
                //Ocultamos botones
                $("#OkButton").hide();
                $("#NoButton").hide();
            }
        }
    });
}

//Función para el botón de ok (móvil)
function okBtnMobile() {
    $.ajax({
        type: "POST",
        url: "index.php",
        data: {
            status: "ok",
            userAgent: "mobile"
        },
        dataType: "html",
        success: function () {
            window.location.href = "/IAT/static/src/welcome_mobile.php"
        },
        statusCode: {
            400: function () {
                //Cambiamos el estilo del mensaje principal
                $("#message").toggleClass("noJsMsg");
                //Cambiamos texto del mensaje principal
                $("#message").text("¡Ups! La información enviada por el servidor ha sido comprometida o corrompida. Por favor, intenta más tarde.")
                //Ocultamos botones
                $("#OkButton").hide();
                $("#NoButton").hide();
            }
        }
    });
}

//Función para el boton de cancelar (móvil)
function noBtnMobile() {
    $.ajax({
        type: "POST",
        url: "index.php",
        data: {
            status: "cancel",
            userAgent: "mobile"
        },
        dataType: "html",
        success: function () {
            window.location.href = "/IAT/static/src/welcome.php"
        },
        statusCode: {
            400: function () {
                //Cambiamos el estilo del mensaje principal
                $("#message").toggleClass("noJsMsg");
                //Cambiamos texto del mensaje principal
                $("#message").text("¡Ups! La información enviada por el servidor ha sido comprometida o corrompida. Por favor, intenta más tarde.")
                //Ocultamos botones
                $("#OkButton").hide();
                $("#NoButton").hide();
            }
        }
    });
}

//Función para configurar botones
function setBtns() {
    //Decodificamos tipo de usuario
    const userType_d = b64DecodeUnicode(userType);
    //Asignamos acciones dependiendo del tipo de usuario
    if (userType_d === "desktop") {
        $("#OkButton").click(okBtnDesktop);
        $("#NoButton").click(noBtnDesktop);
    } else if (userType_d === "mobile") {
        $("#OkButton").click(okBtnMobile);
        $("#NoButton").click(noBtnMobile);
    } else {
        //Cambiamos el estilo del mensaje principal
        $("#message").toggleClass("noJsMsg");
        //Cambiamos texto del mensaje principal
        $("#message").text("¡Ups! La información enviada por el servidor ha sido comprometida o corrompida. Por favor, intenta más tarde.")
        //Ocultamos botones
        $("#OkButton").hide();
        $("#NoButton").hide();
    }
}

$(document).ready(function () {
    loadMsg();
    setBtns();
});