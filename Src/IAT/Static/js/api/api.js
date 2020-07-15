class iatAPI {
    //Constructor de API
    constructor() {
        this.endPoints = {
            POST_results: function (payload) {
                $.ajax({
                    type: "POST",
                    url: "api/result",
                    contentType: 'application/json',
                    dataType: "json",
                    data: JSON.stringify(payload),
                    async: false
                });
            },
            GET_results: function (success, error) {
                $.ajax({
                    type: "GET",
                    url: "api/result",
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
                    url: `api/stimuli?stage=${stage}`,
                    dataType: "json",
                    success: success
                });
            }
        }
    };
}