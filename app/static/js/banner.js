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

const selectMessage = document.getElementById("selectMessage");
selectMessage.addEventListener('change', fillBanner)
function fillBanner() {
    let selectMessage = document.getElementById("selectMessage");
    let box = document.getElementById("message");
    box.value = selectMessage.value;
    console.log(x.value)
}