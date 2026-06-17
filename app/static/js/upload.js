async function uploadFile() {
    let passwordOK = await checkPassword();
    if (!passwordOK) { return; }

    if (!checkFileSelected()) { return; }

    let fileExists = await fileAlreadyExistsInDB();
    if (fileExists) { return; }

    document.getElementById("uploadStatus").style.display = "block";

    let data = new FormData();
    const file = document.getElementById("uploadFile").files[0];
    data.append("file", file)
    const password = document.getElementById("uploadPassword").value;
    data.append("password", password)

    const request = new XMLHttpRequest();

    request.upload.addEventListener("progress", function (event) {
        // Get a suitable number for the progress bar. 
        const percent = ((event.loaded / event.total) * 100) - 1;
        const rounded = Math.floor(percent);
        document.getElementById("progress").value = rounded;
        document.getElementById("progressPercent").innerText = rounded + "%"
    })

    request.addEventListener("load", function () {
        if (request.status == 200){
            document.getElementById("progressPercent").innerText = "100%";
            // await new Promise(requestAnimationFrame); // allow time for updating content before alert() box
            alert(`${file.name} successfully uploaded!`);
        } else {
            alert(`Could not upload ${file.name}! Please try again or contact the tech team.`);
            document.getElementById("uploadStatus").style.display = "none";
        }
    })

    const url = "/upload/newfile";
    request.open("PUT", url);
    request.send(data);

}

async function checkPassword() {
    const password = document.getElementById("uploadPassword").value;
    if (!password) {
        modalAlert("you forgot the password");
        return false;
    }

    let toSend = { "password": password };
    let response = await fetch("/upload/checkpassword", {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(toSend)
    })

    if (!response.ok) {
        modalAlert("wrong password");
        return false;
    } else { return true; }
}

function checkFileSelected() {
    const file = document.getElementById("uploadFile").files[0];
    if (!file) {
        modalAlert("no file selected");
        return false;
    } else { return true; }
}

async function fileAlreadyExistsInDB() {
    const filename = document.getElementById("uploadFile").files[0].name;
    const data = { "filename": filename };
    let response = await fetch("/upload/checkduplicate", {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(data)
    })

    if (response.ok) {
        return false;
    }
    let responseJSON = await response.json();
    modalAlert(responseJSON.response);
    return true;
}

window.addEventListener("dragover", (e) => { e.preventDefault() })
window.addEventListener("drop", handleFileDrop)

function handleFileDrop(drop) {
    drop.preventDefault();
    let fileDrop = drop.dataTransfer.files[0]; // only allow one file at a time
    let dataTransfer = new DataTransfer();
    dataTransfer.items.add(fileDrop);
    let element = document.getElementById("uploadFile");
    element.files = dataTransfer.files;

}
