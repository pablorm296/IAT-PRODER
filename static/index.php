<?php
//Importamos librerías
require_once('./libs/Mobile-Detect/Mobile_Detect.php');

//Incluimos la cabecera
require_once('./src/userAgentCheckHeader.php');

//Iniciamos nueva instancia de Mobile_Detect
$detect = new Mobile_Detect();

//Iniciamos una nueva sesión
session_start();

//Verificar si es una petición GET o una petición POST
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    //Verificar el tipo de dispositivo desde el cual el usuario está accediendo
    //Primero verificamos que HTTP_USER_AGENT esté definido en la cabecera de la petición
    if (isset($_SERVER['HTTP_USER_AGENT']) and $_SERVER['HTTP_USER_AGENT'] != '') {

        if ($detect->isMobile()) {
            //Enviamos variables a JS
            //Las variables estarán codificadas en base64
?>
            <!-- PHP var dump -->
            <script>
                const userType = "bW9iaWxl";
                const msgContent = "SGVtb3MgZGV0ZWN0YWRvIHF1ZSB1c2FzIHVuIGRpc3Bvc2l0aXZvIG3Ds3ZpbCAodGFibGV0YSBvIHRlbMOpZm9ubykuIMK/RXMgY29ycmVjdG8/";
                const okButtonTxt = "U8Ot";
                const noButtonTxt = "Tm8sIGVzdG95IHVzYW5kbyB1bmEgY29tcHV0YWRvcmEgZGUgZXNjcml0b3JpbyBvIGxhcHRvcA==";
            </script>
        <?php
            require_once('./html/userAgentCheck.html');
        } else {
            //Enviamos variables a JS
        ?>
            <!-- PHP var dump -->
            <script>
                const userType = "ZGVza3RvcA==";
                const msgContent = "SGVtb3MgZGV0ZWN0YWRvIHF1ZSB1c2FzIHVuYSBjb21wdXRhZG9yYSBkZSBlc2NyaXRvcmlvIG8gbGFwdG9wLiDCv0VzIGNvcnJlY3RvPw==";
                const okButtonTxt = "U8Ot";
                const noButtonTxt = "Tm8sIGVzdG95IHVzYW5kbyB1biBkaXNwb3NpdGl2byBtw7N2aWwgKHRhYmxldGEgbyB0ZWzDqWZvbm8p";
            </script>
        <?php
            require_once('./html/userAgentCheck.html');
        }
    } else {
        ?>
        <!-- PHP var dump -->
        <script>
            const userType = "YW5vbg==";
            const msgContent = "vwqFVcHMhIEVsIGVuY2FiZXphZG8gZGUgdHUgcGV0aWNpw7NuIG5vIGNvbnRpZW5lIGluZm9ybWFjacOzbiBxdWUgbmVjZXNpdGFtb3MgcGFyYSBlbCBjb3JyZWN0byBmdW5jaW9uYW1pZW50byBkZSBsYSBwcnVlYmEuIFNpIHVzYXMgdW4gcGx1Zy1pbiBxdWUgZGVzYWN0aXZhIGNpZXJ0b3MgZW5jYWJlemFkb3MsIGRlc2FjdMOtdmFsby4g";
        </script>
<?php
    }
    //Usuario hace request post
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
    //Comprobamos que se incluyó query status
    if (isset($_POST["status"]) and isset($_POST["userAgent"])) {
        $userStatus = $_POST["status"];
        $userAgent = $_POST["userAgent"];
        //Si el usuario confirma nuestra detección
        if ($userStatus == "ok") {
            if ($detect->isMobile() and $userAgent == "mobile") {
                http_response_code(200);
            } elseif (!$detect->isMobile() and $userAgent == "desktop") {
                http_response_code(200);
            } else {
                http_response_code(400);
            }
            //Si el usuario no confirma nuestra detección
        } elseif ($userStatus == "cancel") {
            http_response_code(200);
        }
    } else {
        http_response_code(400);
    }
}

?>