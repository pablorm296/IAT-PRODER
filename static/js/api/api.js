class iatAPI {
    //Constructor de API
    constructor(host, basePath) {
        this.host = "https://pabloreyes.com.mx/";
        this.alias = "api/versions/1/"
        this.routeBank = {
            POST_newUser: {
                route: "users/new"
            }
        };
        this.endPoints = {
            POST_newUser: function () {
                $.ajax({
                    type: "POST",
                    url: this.getRoute("POST_newUser"),
                    data: JSON.stringify({
                        X_VALIDATOR: "FRT0Zx5s0O"
                    }),
                    dataType: "json",
                    success: function (response) {
                        console.log("Test");
                    }
                });
            }
        };
    }
    // Función para obtener la ruta de un endpoint
    getRoute(endPointName) {
        const route = this.host + this.alias + this.routeBank[endPointName]["route"];
        if (route == null) {
            throw "The endpoint does not exists!";
        } else {
            return route;
        }
    }
}