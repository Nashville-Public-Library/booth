async function schedule(date=undefined) {
    document.getElementById("dots").style.display = 'block'
    const url = `/booth/data`;
    let response = await fetch(url, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
        method: "POST",
        body: JSON.stringify({"date": date})
    });
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
    document.getElementById("dots").style.display = 'none'

}

function check_time() {
    const current_time = new Date()
    var minute = current_time.getMinutes()
    if (minute == 0 || minute == 15 || minute == 30 || minute == 45) {
        submitCalendar()
    }
}

function submitCalendar() {
    let date = document.getElementById("calendar").value;
    let dateSplit = date.split("-")
    let sanatizedDate = `${dateSplit[1]}${dateSplit[2]}${dateSplit[0]}`
    schedule(date=sanatizedDate)
}
submitCalendar()
setInterval(check_time, 60000)