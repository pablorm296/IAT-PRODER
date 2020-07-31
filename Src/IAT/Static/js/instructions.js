// Main KeyHandler
function keyHandler(e, v = false, c) {
    // Init an empty where key code is going to be stored
    var keyCode;

    // Get keycode
    if (window.event) { // IE                    
        keyCode = e.keyCode;
    } else if (e.which) { // Netscape/Firefox/Opera                   
        keyCode = e.which;
    }

    // Get name of pressed key
    var keyName = String.fromCharCode(keyCode);
    // If it's a blank space, it means use pressed space key
    if (keyName === " ") {
        keyName = "space";
    }
    // If there's a callback, send. Else, return keyName
    if (c) {
        c(keyName);
    } else {
        return keyName;
    }
}

// Key Pressed Callback
function keyCallBack(keyName) {
    if (keyName == "space") {
        window.location.href = "/iat";
    }
}

// Ok button function
function okBtn() {
    // Go to instructions page
    window.location.href = "/iat";
}

// Set Buttons actions
function setBtns() {
    // Only if OkButton exists (mobile version)
    if ($("#mydiv").length > 0){
        // Ok button action
        $("#OkButton").click(okBtn);
    }
}

// When document is loaded
$(document).ready(function () {
    // Set buttons
    setBtns();
    // Assign keyHandler to key press event
    $(document).keypress(function (e) {
        e.preventDefault();
        keyHandler(e, false, keyCallBack);
    });
});