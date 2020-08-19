var myAPI;

//Función para validar respuestas del usuario
function checkInput() {
    const compulsoryIndex = [0, 1, 2];
    //Lista de ids
    const idArrays = ["srvy_suggestions", "srvy_felt", "srvy_result"];
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
        return true;
    }

}

function saveResults() {
    // Create answers object
    var answers = {};
    // Get all input fields
    const all_inputs = $("textarea").toArray();

    for (let index = 0; index < all_inputs.length; index++) {
        const element = all_inputs[index];
        const element_id = element.id;
        var element_value = element.value;
        // Add to answers obj
        answers[element_id] = element_value;

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
    myAPI.endPoints.POST_debugSurvey(answers, function () {
        alert("Muchas gracias por haber participado en esta prueba piloto. Tus respuestas nos ayudarán a mejorar el IAT.")
        window.location.href = "https://discriminacion.colmex.mx/";
    });
}

//Función para el botón de ok
function okBtn() {
    //Validamos
    if (checkInput()) {
        // Emviamos respuesas
        saveResults();
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