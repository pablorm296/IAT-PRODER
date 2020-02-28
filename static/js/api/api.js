//Función para guardar una cookie
function saveCookie(name, value, expiration, maxAge, path = "/") {
    //Verificar parametros
    if (typeof name === "undefined") {
        throw "Cookie name is not defined!"
    }
    if (typeof value === "undefined") {
        throw "Cookie value is not defined!"
    }
    if (typeof expiration === "undefined" && typeof maxAge === "undefined") {
        throw "Cookie must have an expiration or a maxAge parameter!"
    }
    if (expiration && maxAge) {
        throw "Can't define expiration and maxAge at the same time!"
    }
    if (typeof path === "undefined") {
        throw "Cookie path is no defined!"
    }
    //Definir expiración
    if (expiration) {
        //Definir con expiración
        const timeStamp = new Date().getTime();
        const expiration = timeStamp + (60 * 60 * 24 * 1000);
        const expirationStr = "expires=" + expiration.toGMTString();
        //Definir str de cookie
        const cookieStr = `${name}=${value}; ${expirationStr}; path=${path}`;
        //Establecemos cookie
        document.cookie = cookieStr;
        return true;
    } else if (maxAge) {
        //Definir edad máxima
        const maxAgeStr = "max-age=" + maxAge;
        //Definir str de cookie
        const cookieStr = `${name}=${value}; ${maxAgeStr}; path=${path}`;
        //Establecemos cookie
        document.cookie = cookieStr;
        return true;
    }

}

//Interfaz de la API
class iatAPI {
    //Constructor de API
    constructor() {
        this.host = "https://pabloreyes.com.mx/";
        this.alias = "api/versions/1/"
        this.endPoints = {
            POST_newUser: function () {
                $.ajax({
                    type: "POST",
                    url: "https://pabloreyes.com.mx/api/versions/1/users/new",
                    data: JSON.stringify({
                        "X_VALIDATOR": "RlJUMFp4NXMwTw=="
                    }),
                    contentType: 'application/json',
                    dataType: "json",
                    success: function (data) {
                        //Seleccionar objeto de interés
                        const responseContent = data.responseContent;
                        //Guardar id en una cookie
                        const userId = responseContent.id;
                        if (userId) {
                            saveCookie("appSession", userId, undefined, 86400);
                        } else {
                            throw "Can't parse user id";
                        }
                    }
                });
            }
        };
    }
}