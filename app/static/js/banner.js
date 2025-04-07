document.getElementById("selectMessage").addEventListener('change', fillBanner)
function fillBanner() {
    let selectMessage = document.getElementById("selectMessage");
    let box = document.getElementById("bannerMessage");
    box.value = selectMessage.value;
}

function validateBanner() {
    password = document.getElementById('password');
    if (password.value == '') {
        success = document.getElementById('success');
        success.style.display = 'block'
        // clear the emoji
        emoji = document.getElementById('emoji');
        emoji.remove()
    }
    else {
        form = document.getElementById('banner');
        form.submit();
    }
}

async function bannerContent() {
    const url = "/booth/banner/content"
    const options = {method: "POST"}
    let response = await fetch(url, options)
    let responseJSON = await response.json()

    const bannerColorElement = document.getElementById("bannerColor");
    const bannerMessageElement = document.getElementById("bannerMessage")

    bannerMessageElement.innerText = responseJSON.banner

    if (responseJSON.bannerColor) {
        bannerColorElement.value = responseJSON.bannerColor
    }
    else{
        // default to red if none chosen
        bannerColorElement.value = "#a52a2a"
    }

    // if there is no message, change the default color back to red
    if (!responseJSON.banner) {
        bannerColorElement.value = "#a52a2a"
    }
}

window.onload = bannerContent()