/**
 * Calls cbfun with xhr request,
 * resulting from sending data to
 * syntax highlighter
 */
function requestSyntax(language, code, cbfun) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", window.location.origin + "/syntax.py", true);

    xhr.onreadystatechange= function () {
        if (this.readyState == XMLHttpRequest.DONE) {
            cbfun(this);
        }
    };

    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
        "fun":"highlight",
        "lang":language,
        "data":code
    }));
}

/**
 * Auto adds syntax to element
 */
function autoSyntax(language, code, element) {
    requestSyntax(language, code, function(xhr) {
       element.innerHTML = xhr.response;
    });
}