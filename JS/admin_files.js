function uploadFile() {
    var msgbar = document.getElementById("messagebar");
    var alertdiv = document.createElement("div");
    alertdiv.classList.add("alert");
    alertdiv.classList.add("alert-info");
    var par = document.createElement("p");
    par.innerHTML = "<strong>Please Wait!</strong> Uploading your file"
    alertdiv.appendChild(par);
    msgbar.appendChild(alertdiv);

    var form = document.getElementById("file-upload-form");
    var apikey = document.getElementById("Authorizationupload").value;
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var FileName = document.getElementById("FileName").value;
    const apiendpoint = "/api/admin/uploadfile"
    var xhr = new XMLHttpRequest();
    xhr.open("POST", apiendpoint);
    xhr.setRequestHeader("username", username);
    xhr.setRequestHeader("password", password);
    xhr.setRequestHeader("Auth", apikey);
    xhr.setRequestHeader('FileName', FileName)
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
            var uploadurl = resp["FileLink"]

            $(".alert").alert('close');

            var msgbar = document.getElementById("messagebar");
            var alertdiv = document.createElement("div");
            alertdiv.classList.add("alert");
            alertdiv.classList.add("alert-info");
            var par = document.createElement("p");
            par.innerHTML = "<strong>Done!</strong> Redirecting you to the file link"
            alertdiv.appendChild(par);
            msgbar.appendChild(alertdiv);
            setTimeout(function () { document.location.replace(uploadurl); }, 2000);
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

function deleteFile() {
    var msgbar = document.getElementById("messagebar");
    var alertdiv = document.createElement("div");
    alertdiv.classList.add("alert");
    alertdiv.classList.add("alert-info");
    var par = document.createElement("p");
    par.innerHTML = "<strong>Please Wait!</strong> Deleting file"
    alertdiv.appendChild(par);
    msgbar.appendChild(alertdiv);

    var form = document.getElementById("file-delete-form");
    var apikey = document.getElementById("Authorizationfdel").value;
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var FileName = document.getElementById("FileNamedel").value;
    const apiendpoint = "/api/admin/deletefile"
    var xhr = new XMLHttpRequest();
    xhr.open("DELETE", apiendpoint);
    xhr.setRequestHeader("username", username);
    xhr.setRequestHeader("password", password);
    xhr.setRequestHeader("Auth", apikey);
    xhr.setRequestHeader('FileName', FileName)
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
            par.innerHTML = "<strong>Warning!</strong> An error occured, got code " + resp["Status"] + " from server!"
            alertdiv.appendChild(par);
            msgbar.appendChild(alertdiv);
            setTimeout(function () { $(".alert").alert('close'); }, 5000);
        }
    }
    xhr.send(data);
}

function renameFile() {
    var msgbar = document.getElementById("messagebar");
    var alertdiv = document.createElement("div");
    alertdiv.classList.add("alert");
    alertdiv.classList.add("alert-info");
    var par = document.createElement("p");
    par.innerHTML = "<strong>Please Wait!</strong> Renaming file"
    alertdiv.appendChild(par);
    msgbar.appendChild(alertdiv);

    var form = document.getElementById("file-rename-form");
    var apikey = document.getElementById("Authorizationfren").value;
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var oldFileName = document.getElementById("oldFileNameren").value;
    var newFileName = document.getElementById("newFileNameren").value;
    const apiendpoint = "/api/admin/renamefile"
    var xhr = new XMLHttpRequest();
    xhr.open("PUT", apiendpoint);
    xhr.setRequestHeader("username", username);
    xhr.setRequestHeader("password", password);
    xhr.setRequestHeader("Auth", apikey);
    xhr.setRequestHeader('oldfilename', oldFileName);
    xhr.setRequestHeader('newfilename', newFileName);
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
    xhr.send(data);
}

function loadFiles() {
    var msgbar = document.getElementById("messagebar");
    var alertdiv = document.createElement("div");
    alertdiv.classList.add("alert");
    alertdiv.classList.add("alert-info");
    var par = document.createElement("p");
    par.innerHTML = "<strong>Please Wait!</strong> Loading files"
    alertdiv.appendChild(par);
    msgbar.appendChild(alertdiv);

    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    const apiendpoint = "/api/admin/listfiles"
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

            var selectfiles = document.getElementById("files")

            resp["files"].forEach(function (file) {
                var selector = document.createElement("option");
                selector.innerHTML = file;
                selector.value = file;
                selectfiles.appendChild(selector)
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
