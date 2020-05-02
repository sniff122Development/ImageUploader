function genAPIkey() {
    var msgbar = document.getElementById("messagebar");
    var alertdiv = document.createElement("div");
    alertdiv.classList.add("alert");
    alertdiv.classList.add("alert-info");
    var par = document.createElement("p");
    par.innerHTML = "<strong>Please Wait!</strong> Generating new API key"
    alertdiv.appendChild(par);
    msgbar.appendChild(alertdiv);

    var form = document.getElementById("apigen-form");
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var name = document.getElementById("apigenname").value;
    const apiendpoint = "/api/admin/newkey"
    var xhr = new XMLHttpRequest();
    xhr.open("GET", apiendpoint);
    xhr.setRequestHeader("username", username);
    xhr.setRequestHeader("password", password);
    xhr.setRequestHeader("name", name)
    var data = new FormData(form);
    xhr.onload = function () {
        var resp = JSON.parse(this.responseText);
        if (resp["Status"] == 401) {
            $(".alert").alert('close');
            var msgbar = document.getElementById("messagebar");
            var alertdiv = document.createElement("div");
            alertdiv.classList.add("alert");
            alertdiv.classList.add("alert-danger");
            var par = document.createElement("p");
            par.innerHTML = "<strong>Unauthorized!</strong> You are not authorized to do that!"
            alertdiv.appendChild(par);
            msgbar.appendChild(alertdiv);
            setTimeout(function () { $(".alert").alert('close'); }, 5000);
        } else if (resp["Status"] == 200) {
            $(".alert").alert('close');

            var msgbar = document.getElementById("messagebar");
            var alertdiv = document.createElement("div");
            alertdiv.classList.add("alert");
            alertdiv.classList.add("alert-info");
            var par = document.createElement("p");
            par.innerHTML = "<strong>Done!</strong> API Key: " + resp["newkey"]
            alertdiv.appendChild(par);
            msgbar.appendChild(alertdiv);
        } else {
            $(".alert").alert('close');

            var msgbar = document.getElementById("messagebar");
            var alertdiv = document.createElement("div");
            alertdiv.classList.add("alert");
            alertdiv.classList.add("alert-danger");
            var par = document.createElement("p");
            par.innerHTML = "<strong>Warning!</strong> An error occured, got code " + resp["Status"] + " from server! " + resp["Message"]
            alertdiv.appendChild(par);
            msgbar.appendChild(alertdiv);
            setTimeout(function () { $(".alert").alert('close'); }, 5000);
        }
    }
    xhr.send(data);
}

function revokeAPIkey() {
    var msgbar = document.getElementById("messagebar");
    var alertdiv = document.createElement("div");
    alertdiv.classList.add("alert");
    alertdiv.classList.add("alert-info");
    var par = document.createElement("p");
    par.innerHTML = "<strong>Please Wait!</strong> Revoking API key"
    alertdiv.appendChild(par);
    msgbar.appendChild(alertdiv);

    var form = document.getElementById("apirevoke-form");
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var key = document.getElementById("apirevokekey").value;
    const apiendpoint = "/api/admin/revokekey"
    var xhr = new XMLHttpRequest();
    xhr.open("DELETE", apiendpoint);
    xhr.setRequestHeader("username", username);
    xhr.setRequestHeader("password", password);
    xhr.setRequestHeader("key", key)
    var data = new FormData(form);
    xhr.onload = function () {
        var resp = JSON.parse(this.responseText);
        if (resp["Status"] == 401) {
            $(".alert").alert('close');
            var msgbar = document.getElementById("messagebar");
            var alertdiv = document.createElement("div");
            alertdiv.classList.add("alert");
            alertdiv.classList.add("alert-danger");
            var par = document.createElement("p");
            par.innerHTML = "<strong>Unauthorized!</strong> You are not authorized to do that!"
            alertdiv.appendChild(par);
            msgbar.appendChild(alertdiv);
            setTimeout(function () { $(".alert").alert('close'); }, 5000);
        } else if (resp["Status"] == 200) {
            $(".alert").alert('close');

            var msgbar = document.getElementById("messagebar");
            var alertdiv = document.createElement("div");
            alertdiv.classList.add("alert");
            alertdiv.classList.add("alert-info");
            var par = document.createElement("p");
            par.innerHTML = "<strong>Done!</strong> API key revoked!"
            alertdiv.appendChild(par);
            msgbar.appendChild(alertdiv);
        } else {
            $(".alert").alert('close');

            var msgbar = document.getElementById("messagebar");
            var alertdiv = document.createElement("div");
            alertdiv.classList.add("alert");
            alertdiv.classList.add("alert-danger");
            var par = document.createElement("p");
            par.innerHTML = "<strong>Warning!</strong> An error occured, got code " + resp["Status"] + " from server! " + resp["Message"]
            alertdiv.appendChild(par);
            msgbar.appendChild(alertdiv);
            setTimeout(function () { $(".alert").alert('close'); }, 5000);
        }
    }
    xhr.send(data);
}