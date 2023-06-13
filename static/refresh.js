// refresh page
function refresh_page() {
    window.location.reload();
}
function check_time() {
    const current_time = new Date()
    var minute = current_time.getMinutes()
    if (minute == 0 || minute == 30) {
        refresh_page()
    }
}
setInterval(check_time, 60000)