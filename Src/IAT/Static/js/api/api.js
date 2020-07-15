class iatAPI {
    //Constructor de API
    constructor() {
        this.host = "http://127.0.0.1/";
        this.alias = "api/"
        this.endPoints = {
            POST_results: function (payload) {
                $.ajax({
                    type: "POST",
                    url: `${this.host}${this.alias}/result`,
                    contentType: 'application/json',
                    dataType: "json",
                    data: JSON.stringify(payload),
                    async: false
                });
            },
            GET_results: function (success, error) {
                $.ajax({
                    type: "GET",
                    url: `${this.host}${this.alias}/result`,
                    contentType: 'application/json',
                    dataType: "json",
                    async: false,
                    success: success,
                    error: error
                });
            },
            GET_stimuli: function (stage, success, error) {
                $.ajax({
                    type: "GET",
                    url: `${this.host}${this.alias}/stimuli`,
                    dataType: "json",
                    success: success
                });
            }
        }
    };
}