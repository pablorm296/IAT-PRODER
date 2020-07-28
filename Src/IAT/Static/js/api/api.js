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
                    async: false,
                    error: function() {alert("An unexpected error occurred when posting the test results! Please contact server admin"); window.location.href = "https://www.discriminacion.colmex.mx/";}
                });
            },
            POST_survey: function (payload, success) {
                $.ajax({
                    type: "POST",
                    url: "api/survey",
                    contentType: 'application/json',
                    dataType: "json",
                    data: JSON.stringify(payload),
                    success: success,
                    error: function() {alert("An unexpected error occurred when posting the survey results! Please contact server admin"); window.location.href = "https://www.discriminacion.colmex.mx/";}
                });
            },
            GET_results: function (success) {
                $.ajax({
                    type: "GET",
                    url: "api/result",
                    contentType: 'application/json',
                    dataType: "json",
                    success: success,
                    error: function() {alert("An unexpected error occurred when getting the test results! Please contact server admin"); window.location.href = "https://www.discriminacion.colmex.mx/";}
                });
            },
            GET_stimuli: function (stage, success) {
                $.ajax({
                    type: "GET",
                    url: `api/stimuli?stage=${stage}`,
                    dataType: "json",
                    success: success,
                    error: function() {alert("An unexpected error occurred when getting the test stimuli! Please contact server admin"); window.location.href = "https://www.discriminacion.colmex.mx/";}
                });
            }
        }
    };
}