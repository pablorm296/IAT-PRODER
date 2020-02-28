class iatAPI {
    //Constructor de API
    constructor(host, basePath) {
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
                    success: function (response) {
                        console.log("test");
                    }
                });
            }
        };
    }
}