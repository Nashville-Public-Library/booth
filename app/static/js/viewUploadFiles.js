        async function deleteItem(item) {
            const url = "/upload/deletefile";
            let file = {"filename": item}
            let response = await fetch(url, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                method: "DELETE",
                body: JSON.stringify(file)
            })
            if (!response.ok){
                alert(`something went wrong! could not delete ${item}`)
            }
            let responseJSON = await response.json();
            console.log(responseJSON);
            window.location.reload();
        }

        async function fetchFile(downloadURL) {
            const file = {"token": downloadURL}
            const url = "/upload/fetchfile"
            let response = await fetch(url, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                method: "POST",
                body: JSON.stringify(file)
            });
            if (response.ok) {
                let responseJSON = await response.json();
                window.open(responseJSON.url, "_blank");
            } else {
                alert("There was a problem unencrypting and downloading the file...")
            }
        }