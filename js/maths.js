function solve(equation, toSolveFor, cbfun) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", window.location.origin + "/maths.py", true);

    xhr.onreadystatechange= function () {
        if (this.readyState == XMLHttpRequest.DONE) {
            cbfun(this);
        }
    };

    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
        "fun":"solve",
        "eq":equation,
        "val":toSolveFor
    }));
}

function toLatex(equation, cbfun) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", window.location.origin + "/maths.py", true);

    xhr.onreadystatechange= function () {
        if (this.readyState == XMLHttpRequest.DONE) {
            cbfun(this);
        }
    };

    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
        "fun":"toLatex",
        "eq":equation
    }));
}