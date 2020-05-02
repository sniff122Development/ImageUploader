function shortLink() {
    var msgbar = document.getElementById("messagebar");
    var alertdiv = document.createElement("div");
    alertdiv.classList.add("alert");
    alertdiv.classList.add("alert-info");
    var par = document.createElement("p");
    par.innerHTML = "<strong>Please Wait!</strong> Shortening your link"
    alertdiv.appendChild(par);
    msgbar.appendChild(alertdiv);

    var apikey = document.getElementById("Authorizationlnew").value;
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var shortlink = document.getElementById("linkname").value;
    var longlink = document.getElementById("linkurl").value;
    const apiendpoint = "/api/admin/url"
    var xhr = new XMLHttpRequest();
    xhr.open("POST", apiendpoint);
    xhr.setRequestHeader("username", username);
    xhr.setRequestHeader("password", password);
    xhr.setRequestHeader("Auth", apikey);
    xhr.setRequestHeader('url', longlink)
    xhr.setRequestHeader('id', shortlink)
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
            var shorturl = resp["shorturl"]

            $(".alert").alert('close');

            var msgbar = document.getElementById("messagebar");
            var alertdiv = document.createElement("div");
            alertdiv.classList.add("alert");
            alertdiv.classList.add("alert-info");
            var par = document.createElement("p");
            par.innerHTML = "<strong>Done!</strong> Short Link: " + shorturl
            alertdiv.appendChild(par);
            msgbar.appendChild(alertdiv);
            setTimeout(function () { $(".alert").alert('close'); }, 10000);
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
    xhr.send();
}

function deleteLink() {
    var msgbar = document.getElementById("messagebar");
    var alertdiv = document.createElement("div");
    alertdiv.classList.add("alert");
    alertdiv.classList.add("alert-info");
    var par = document.createElement("p");
    par.innerHTML = "<strong>Please Wait!</strong> Deleting link"
    alertdiv.appendChild(par);
    msgbar.appendChild(alertdiv);

    var apikey = document.getElementById("Authorizationldel").value;
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var LinkName = document.getElementById("LinkDel").value;
    const apiendpoint = "/api/admin/deletelink"
    var xhr = new XMLHttpRequest();
    xhr.open("DELETE", apiendpoint);
    xhr.setRequestHeader("username", username);
    xhr.setRequestHeader("password", password);
    xhr.setRequestHeader("Auth", apikey);
    xhr.setRequestHeader('id', LinkName)
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
            par.innerHTML = "<strong>Done!</strong>"
            alertdiv.appendChild(par);
            msgbar.appendChild(alertdiv);
            setTimeout(function () { $(".alert").alert('close'); }, 5000);
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
    xhr.send();
}

function renameLink() {
    var msgbar = document.getElementById("messagebar");
    var alertdiv = document.createElement("div");
    alertdiv.classList.add("alert");
    alertdiv.classList.add("alert-info");
    var par = document.createElement("p");
    par.innerHTML = "<strong>Please Wait!</strong> Renaming link"
    alertdiv.appendChild(par);
    msgbar.appendChild(alertdiv);

    var form = document.getElementById("link-rename-form");
    var apikey = document.getElementById("Authorizationlren").value;
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var oldLinkName = document.getElementById("oldlink").value;
    var newLinkName = document.getElementById("newlink").value;
    const apiendpoint = "/api/admin/renamelink"
    var xhr = new XMLHttpRequest();
    xhr.open("PUT", apiendpoint);
    xhr.setRequestHeader("username", username);
    xhr.setRequestHeader("password", password);
    xhr.setRequestHeader("Auth", apikey);
    xhr.setRequestHeader('oldid', oldLinkName);
    xhr.setRequestHeader('newid', newLinkName);
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
            par.innerHTML = "<strong>Done!</strong>"
            alertdiv.appendChild(par);
            msgbar.appendChild(alertdiv);
            setTimeout(function () { $(".alert").alert('close'); }, 5000);
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
    xhr.send();
}

function loadLinks() {
    var msgbar = document.getElementById("messagebar");
    var alertdiv = document.createElement("div");
    alertdiv.classList.add("alert");
    alertdiv.classList.add("alert-info");
    var par = document.createElement("p");
    par.innerHTML = "<strong>Please Wait!</strong> Loading Links"
    alertdiv.appendChild(par);
    msgbar.appendChild(alertdiv);

    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    const apiendpoint = "/api/admin/listlinks"
    var xhr = new XMLHttpRequest();
    xhr.open("GET", apiendpoint);
    xhr.setRequestHeader("username", username);
    xhr.setRequestHeader("password", password);
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
            par.innerHTML = "<strong>Done!</strong>"
            alertdiv.appendChild(par);
            msgbar.appendChild(alertdiv);

            var selectlinks = document.getElementById("links")

            resp["links"].forEach(function (link) {
                var selector = document.createElement("option");
                selector.innerHTML = link;
                selector.value = link;
                selectlinks.appendChild(selector)
            });
            setTimeout(function () { $(".alert").alert('close'); }, 5000);
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
    xhr.send();
}
