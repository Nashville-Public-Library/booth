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
selectMessage.addEventListener('click', fillBanner)
function fillBanner() {
    const x = document.getElementById("selectMessage");
    const y = x.value
    const box = document.getElementById("message");
    box.value = x.value;
    console.log(x.value)
}