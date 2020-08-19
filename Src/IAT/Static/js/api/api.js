class iatAPI {
    //Constructor de API
    constructor() {
        this.endPoints = {
            POST_results: function (payload) {
                $.ajax({
                    type: "POST",
                    url: "api/iat/results",
                    contentType: 'application/json',
                    dataType: "json",
                    data: JSON.stringify(payload),
                    async: false,
                    error: function() {window.location.href = "/errorCustom?msg=An unexpected error occurred when posting the test results! Please contact server admin.";}
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
                    error: function() {window.location.href = "/errorCustom?msg=An unexpected error occurred when posting the survey results! Please contact server admin.";}
                });
            },
            POST_debugSurvey: function (payload, success) {
                $.ajax({
                    type: "POST",
                    url: "api/debugSurvey",
                    contentType: 'application/json',
                    dataType: "json",
                    data: JSON.stringify(payload),
                    success: success,
                    error: function() {window.location.href = "/errorCustom?msg=An unexpected error occurred when posting the survey results! Please contact server admin.";}
                });
            },
            GET_stimuli: function (stage, success) {
                $.ajax({
                    type: "GET",
                    url: `api/iat/stimuli?stage=${stage}`,
                    dataType: "json",
                    success: success,
                    error: function() {window.location.href = "/errorCustom?msg=An unexpected error occurred when getting the test stimuli! Please contact server admin.";}
                });
            }
        }
    };
}