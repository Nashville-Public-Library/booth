async function deleteItem(item) {
    const url = "/upload/deletefile";
    let file = { "filename": item }
    let response = await fetch(url, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "DELETE",
        body: JSON.stringify(file)
    })
    if (!response.ok) {
        alert(`something went wrong! could not delete ${item}`)
    }
    let responseJSON = await response.json();
    console.log(responseJSON);
    window.location.reload();
}

async function fetchFile(filename) {
    const url = "/upload/fetchfile/" + filename
    try {
        window.open(url, "_blank");
    }
    catch {
        alert("There was a problem downloading the file...")
    }
}

function NoFiles() {
    const element = document.getElementById("files");    
    const count = element.children.length;
    if (count == 1) {
        document.getElementById("noFiles").style.display = "block" 
    }
}

NoFiles()
