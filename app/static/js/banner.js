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