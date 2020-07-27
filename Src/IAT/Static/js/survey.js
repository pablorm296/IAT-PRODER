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
    // Get edad
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

// Function that configures input checks
function setChecks() {
    // Bind to age on change
    $("#srvy_age").change(numericCheck);
}

// Numeric input check
function numericCheck(value) {
    // Regex that checks if input has somethong that is not a digit
    var re = new RegExp(/\D/);
    var match = re.exec(value);
    // Check match
    if (match !== null) {
        // remove all non numerics
        var user_input = this.value;
        user_input = user_input.replace(re, "");
        this.value = user_input;
        return true;
    }
    return true;
}

//Cuando el documento se carga
$(document).ready(function () {
    // Set buttons
    setBtns();
    // Init API connector
    myAPI = new iatAPI()
});