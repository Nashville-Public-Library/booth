document.getElementById("selectMessage").addEventListener('change', fillBanner)
function fillBanner() {
    let selectMessage = document.getElementById("selectMessage");
    let box = document.getElementById("message");
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

async function bannerColor() {
    const url = "/booth/banner/content"
    const options = {method: "POST"}
    let response = await fetch(url, options)
    let responseJSON = await response.json()
    let color = responseJSON.bannerColor

    const bannerColorElement = document.getElementById("bannerColor");

    if (color) {
        bannerColorElement.value = color
    }
    else{
        bannerColorElement.value = "#a52a2a"
    }
}

bannerColor()