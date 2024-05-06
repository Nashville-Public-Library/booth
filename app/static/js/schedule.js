async function schedule() {
    const url = "/booth/data";
    let response = await fetch(url, { method: "POST" });
    let responseJSON = await response.json();
    document.getElementById("newspaper").innerText = `Newspaper: ${responseJSON.newspaper}`;

    document.getElementById("9-booth1").innerText = responseJSON[9].booth1;
    document.getElementById("9-booth2").innerText = responseJSON[9].booth2;
    document.getElementById("9-booth3").innerText = responseJSON[9].booth3;

    document.getElementById("10-booth1").innerText = responseJSON[10].booth1;
    document.getElementById("10-booth2").innerText = responseJSON[10].booth2;
    document.getElementById("10-booth3").innerText = responseJSON[10].booth3;

    document.getElementById("11-booth1").innerText = responseJSON[11].booth1;
    document.getElementById("11-booth2").innerText = responseJSON[11].booth2;
    document.getElementById("11-booth3").innerText = responseJSON[11].booth3;

    document.getElementById("12-booth1").innerText = responseJSON[12].booth1;
    document.getElementById("12-booth2").innerText = responseJSON[12].booth2;
    document.getElementById("12-booth3").innerText = responseJSON[12].booth3;

    document.getElementById("13-booth1").innerText = responseJSON[13].booth1;
    document.getElementById("13-booth2").innerText = responseJSON[13].booth2;
    document.getElementById("13-booth3").innerText = responseJSON[13].booth3;

    document.getElementById("14-booth1").innerText = responseJSON[14].booth1;
    document.getElementById("14-booth2").innerText = responseJSON[14].booth2;
    document.getElementById("14-booth3").innerText = responseJSON[14].booth3;

    document.getElementById("15-booth1").innerText = responseJSON[15].booth1;
    document.getElementById("15-booth2").innerText = responseJSON[15].booth2;
    document.getElementById("15-booth3").innerText = responseJSON[15].booth3;

    //remove "dots" from page
    document.getElementById("dots").remove()

    // remove border from ALL elements
    var allElements = document.getElementsByTagName('div');
    for (var i = 0; i < allElements.length; i++) {
        allElements[i].classList.remove('schedule-border');
    }

    // add border to current hour
    const date = new Date();
    const hour = date.getHours();
    try {
        if (hour == 8) {
            hour = 9
        }
        if (hour == 16) {
            hour = 15
        }
    document.getElementById(hour).classList.add("schedule-border");
    }
    catch {
        console.log('before 8am, after 5pm')
    }
}

function check_time() {
    const current_time = new Date()
    var minute = current_time.getMinutes()
    if (minute == 0 || minute == 15 || minute == 30 || minute == 45) {
        schedule()
    }
}
schedule()
setInterval(check_time, 60000)