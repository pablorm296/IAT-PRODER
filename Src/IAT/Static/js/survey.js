var myAPI;

//Función para validar respuestas del usuario
function checkInput() {
    const compulsoryIndex = [0, 1, 6, 7];
    //Lista de ids
    const idArrays = ["srvy_age", "srvy_sex", "srvy_lab", "srvy_contry", "srvy_state", "srvy_zip", "srvy_iat", "srvy_hand"];
    //Lista de inputs
    var elemArray = [];
    //Creamos un contador de errores
    var emptyFields = 0;
    //Iteramos por cada elemento
    for (let index = 0; index < idArrays.length; index++) {
        //Obtenemos el id del lemento
        const idString = idArrays[index];
        //Guardamos el elemento en el array
        elemArray.push($(`#${idString}`));   
    }
    //Verificamos que los inputs obligatorios están llenos
    for (let index = 0; index < compulsoryIndex.length; index++) {
        //Obtener índice de elemento obligatorio
        const j = compulsoryIndex[index];
        //Obtener elemento obligatorio
        const element = elemArray[j];
        //Obtener string del elemento obligatorio
        const idStr = idArrays[j];
        //Si está vacío o es none, mandamos error
        const elementValue = element.val();

        if (elementValue == "" || elementValue == "NONE") {
            //Agregamos uno a los campos vacíos
            emptyFields += 1;
            //Cambiamos el estilo de la pregunta en cuestión
            $(`#${idStr}_label`).removeClass("input_label");
            $(`#${idStr}_label`).addClass("input_label_error");
            $(`#${idStr}_label_rm`).removeClass("required_mark");
            $(`#${idStr}_label_rm`).addClass("required_mark_error");
        } else {
            $(`#${idStr}_label`).removeClass("input_label_error");
            $(`#${idStr}_label_rm`).removeClass("required_mark_error");
        }
    }
    // Verificamos reCaptcha
    if (grecaptcha.getResponse() == "") {
        $("#srvy_captcha_label").removeClass("input_label");
        $("#srvy_captcha_label").addClass("input_label_error");
        $("#srvy_captcha_label_rm").removeClass("required_mark");
        $("#srvy_captcha_label_rm").addClass("required_mark_error");
    } else {
        $("#srvy_captcha_label").removeClass("input_label_error");
        $("#srvy_captcha_label").addClass("input_label");
        $("#srvy_captcha_label_rm").removeClass("required_mark_error");
        $("#srvy_captcha_label_rm").addClass("required_mark");
    }
    //Si hay más de un campo vacío, enviamos alerta
    if (emptyFields > 0) {
        alert("Por favor, contesta todas las preguntas obligatorias (marcadas con un asterisco). Hemos marcado en rojo las que olvidaste");
        return false;
    } else {
        //Enviamos resultados
        saveResults();
        return true;
    }

}

function saveResults() {
    // Create answers object
    var answers = {};
    // Get all input fields
    const all_inputs = $("input").toArray();
    // Get all select fields
    const all_selects = $("select").toArray();
    // Merge
    const all_fields = [].concat(all_inputs, all_selects);
    // Loop through fields
    for (let index = 0; index < all_fields.length; index++) {
        const element = all_fields[index];
        const element_id = element.id;
        var element_value = element.value;
        // Checks for select
        if (element.tagName == "SELECT") {
            // Check if value is valid
            if ( (element_value > 100 || element_value < 1) && element_value != "NONE" ) {
                alert("Algunos campos tienen valores inesperados. ¿Estás modificándo los campos con la consola de desarrollador? Si no es así, reporta este error al administrador, por favor");
                throw {name: "spoofedValueError", message: "Unexpected field value. Please, stop using dev console to change user input values."};
            }
            // Add to answers obj
            answers[element_id] = element_value;
        }
        // Checks for inputs
        if (element.tagName == "INPUT") {
            // Numeric inputs
            if (element.type == "tel") {
                // Check that the value is only numeric chars
                const re = new RegExp(/(\D+)/gi);
                const match = re.exec(element_value);
                // Check match
                if (match != null) {
                    alert("Algunos campos tienen valores inesperados. ¿Estás modificándo los campos con la consola de desarrollador? Si no es así, reporta este error al administrador, por favor");
                    throw {name: "spoofedValueError", message: "Unexpected field value. Please, stop using dev console to change user input values."};
                }
                // Check if empty string
                if (element_value === "") {
                    element_value = "NONE";
                }
            }
            // Text inputs
            if (element.type == "text") {
                // Check that the value is only numeric chars
                const re = new RegExp(/[\{\}\*\_\$\%\<\>\#\|\&\?\!\¡\¿\[\]]+/gi);
                const match = re.exec(element_value);
                // Check match
                if (match != null) {
                    alert("Algunos campos tienen valores inesperados. ¿Estás modificándo los campos con la consola de desarrollador? Si no es así, reporta este error al administrador, por favor");
                    throw {name: "spoofedValueError", message: "Unexpected field value. Please, stop using dev console to change user input values."};
                }
                // Check if empty string
                if (element_value === "") {
                    element_value = "NONE";
                }
            }
            if (element.type == "radio") {
                // Get row name
                const row_name = element.name;
                // If row name is already in object, jump to next iteration
                if (answers.hasOwnProperty(row_name)) {
                    continue;
                }
                // Get name value
                var row_value = $(`input[name=${row_name}]:checked`).val();
                // Check undefined values
                if (typeof row_value === "undefined") {
                    row_value = "NONE";
                }
                // Add to answers_obj
                answers[row_name] = row_value;
                // Jump to next iteration
                continue;
            }
            // Add to answers obj
            answers[element_id] = element_value;
        }
    }
    // Get google captcha
    const gResponse = grecaptcha.getResponse();
    // Check google capthca
    if (gResponse === "") {
        alert("Parece que estás intentando saltarte la verificación de reCaptcha. Si no es así, reporta este error al administrador");
        throw {name: "spoofedValueError", message: "Empty reCaptcha. Please, stop using dev console to change user input values."};
    }
    answers["g"] = gResponse;
    // Post answers
    console.log(answers);
    myAPI.endPoints.POST_survey(answers);
}

//Función para el botón de ok
function okBtn() {
    //Validamos y guardamos resultados
    if (checkInput()) {
         //Ir a página de resultados
        window.location.href = "/results";
    }
}

//Función para configurar botones
function setBtns() {
    //Botón ok
    $("#OkButton").click(okBtn);
}

// Function that allows only numeric inputs
function onlyNumeric() {
    //Get element id
    const idName = this.id;
    // Regex that checks if input has somethong that is not a digit
    const current_value = $(`#${idName}`).val();
    const re = new RegExp(/(\D+)/gi);
    const match = re.exec(current_value);
    // Check match
    if (match != null) {
        // remove user input
        $(`#${idName}`).val("");
        // Put error message
        $(`#${idName}_wi`).text("¡Sólo se admiten valores numéricos!");
        $(`#${idName}_wi`).show();
    } else {
        // Hide error message
        $(`#${idName}_wi`).text("");
        $(`#${idName}_wi`).hide();
    }
}

// Function that cleans text input
function onlyGoodCharacters() {
    //Get element id
    const idName = this.id;
    // Regex that checks if input has somethong that is not a digit
    const current_value = $(`#${idName}`).val();
    const re = new RegExp(/[\{\}\*\_\$\%\<\>\#\|\&\?\!\¡\¿\[\]]+/gi);
    const match = re.exec(current_value);
    // Check match
    if (match != null) {
        // remove user input
        $(`#${idName}`).val("");
        // Put error message
        $(`#${idName}_wi`).text("¡Ingresaste uno o más caracteres inválidos!");
        $(`#${idName}_wi`).show();
    } else {
        // Hide error message
        $(`#${idName}_wi`).text("");
        $(`#${idName}_wi`).hide();
    }
}

// Function that configures input checks
function setChecks() {
    // Bind to age on change
    $("#srvy_age").on('change', onlyNumeric);
    // Bind to zip code on change
    $("#srvy_zip").on('change', onlyNumeric);
    // Bind to colonia
    $("#srvy_col").on('change', onlyGoodCharacters);
}

//Cuando el documento se carga
$(document).ready(function () {
    // Set buttons
    setBtns();
    // Set input checks
    setChecks();
});