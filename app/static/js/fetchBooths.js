// fetch booth data and populate elements
async function fetchBooths() {
    let date = new Date();
    let currentHour = date.getHours();
    let nextHour = currentHour + 1;
    if (currentHour == 8) {
        currentHour = 9;
        nextHour = 10
    }
    if (currentHour == 16) {
        currentHour = 15;
        nextHour = 16;
    }
    const booth1_1_display = document.getElementById('Booth1_data');
    const booth2_1_display = document.getElementById('Booth2_data');
    const booth3_1_display = document.getElementById('Booth3_data');
    const booth1_2_display = document.getElementById('Booth1_2_data');
    const booth2_2_display = document.getElementById('Booth2_2_data');
    const booth3_2_display = document.getElementById('Booth3_2_data');
    try {
        const url = "/booth/data";
        var response = await fetch(url, { method: "POST" });
        var responseJSON = await response.json();

        // remove dot-elastic from all elements
        let dots = document.querySelectorAll('.dot-elastic');
        for (let i = 0; i < dots.length; i++) {
            dots[i].classList.remove('dot-elastic');
        }
        booth1_1_display.innerText = responseJSON[currentHour].booth1;
        booth2_1_display.innerText = responseJSON[currentHour].booth2;
        booth3_1_display.innerText = responseJSON[currentHour].booth3;
        if (nextHour >= 16) {
            booth1_2_display.innerText = "CLOSED";
            booth2_2_display.innerText = "CLOSED";
            booth3_2_display.innerText = "CLOSED";
        }
        else {
            booth1_2_display.innerText = responseJSON[nextHour].booth1;
            booth2_2_display.innerText = responseJSON[nextHour].booth2;
            booth3_2_display.innerText = responseJSON[nextHour].booth3;
        }

        document.getElementById('refresh').remove()

        // wait until all elements are populated to italicize
        italicizeMe("Booth1_data")
        italicizeMe("Booth2_data")
        italicizeMe("Booth3_data")
        italicizeMe("Booth1_2_data")
        italicizeMe("Booth2_2_data")
        italicizeMe("Booth3_2_data")
    }
    catch (err) {
        // remove dot-elastic from all elements
        let dots = document.querySelectorAll('.dot-elastic');
        for (let i = 0; i < dots.length; i++) {
            dots[i].classList.remove('dot-elastic');
            }
        let sorry = "?"
        booth1_1_display.innerText = sorry;
        booth2_1_display.innerText = sorry;
        booth3_1_display.innerText = sorry;
        booth1_2_display.innerText = sorry;
        booth2_2_display.innerText = sorry;
        booth3_2_display.innerText = sorry;

        document.getElementById('refresh').remove()
    }
    nowPlaying()
}

/*
italicize empty/closed booth fields
*/
function italicizeMe(x) {
    try {
        var me = document.getElementById(x).textContent;
        if ((me.toLowerCase() == "empty") || (me == "closed")) {
            document.getElementById(x).style.fontStyle = 'italic';
        }
    }
    catch {
        console.log('oh well')
    }
}

async function nowPlaying() {
    let titleElement = document.getElementById('nowPlaying');
    let notAvailable = "Program Name Not Available";
    try {
        const url = "/stream/status";
        let response = await fetch(url, { method: "POST" });
        let icecast = await response.json();
        let nowPlaying = icecast.title;
        if (nowPlaying.trim() == "") {
            titleElement.innerText = notAvailable;
            document.getElementById('nowPlayingContainer').style.display = 'block';
        }
        else {
            titleElement.innerText = nowPlaying;
            document.getElementById('nowPlayingContainer').style.display = 'block';
        }
    }
    catch (whoops) {
        titleElement.innerText = notAvailable;
        document.getElementById('nowPlayingContainer').style.display = 'block';
    }
}

async function fetchBanner() {
    let bannerElement = document.getElementById("banner");
    const url = "/booth/banner/content";
    let response = await fetch(url, { method: "POST" });
    let responseJSON = await response.json();
    if (responseJSON.banner) {
    let bannerColor = responseJSON.bannerColor
    bannerElement.style.borderColor = bannerColor
    bannerElement.innerHTML = responseJSON.banner
    bannerElement.style.display= "block"
    }
}

async function fetchWeatherAlert() {
    let weatherAlertElement = document.getElementById("weatherAlert");
    const url = "/booth/weather/alert";
    let response = await fetch(url, { method: "POST" });
    let responseJSON = await response.json();
    if (responseJSON.alert) {
    weatherAlertElement.innerHTML = responseJSON.alert
    weatherAlertElement.style.display= "block"
    }
}

fetchBanner()
fetchWeatherAlert()
fetchBooths()