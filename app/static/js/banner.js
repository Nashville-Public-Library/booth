document.getElementById("selectMessage").addEventListener('change', fillBanner)
function fillBanner() {
    let selectMessage = document.getElementById("selectMessage");
    let box = document.getElementById("bannerMessage");
    box.value = selectMessage.value;
}

async function submitNewBanner() {
    const bannerElement = document.getElementById("bannerMessage");
    const bannerMessage = bannerElement.value;
    const data = { "bannerMessage": bannerMessage };

    const url = "/booth/banner";
    const options = {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(data)
    };
    let response = await fetch(url, options);
    let responseJSON = await response.json();
    modalAlert(responseJSON.response);
    fetchBanner();
}

async function bannerContent() {
    const url = "/booth/banner/content"
    const options = { method: "POST" }
    let response = await fetch(url, options)
    let responseJSON = await response.json()

    const bannerMessageElement = document.getElementById("bannerMessage")

    bannerMessageElement.innerText = responseJSON.banner
}

window.onload = bannerContent()