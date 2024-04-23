// fetch booth data and populate elements
async function fetchBooths() {
    let date = new Date();
    let currentHour = date.getHours();
    let nextHour = currentHour + 1;
    if (currentHour == 8) {
        currentHour = 9;
        nextHour = 10
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

        nowPlaying()
    }
    catch (err) {
        console.log(err)
    }
}

/*
italicize empty/closed booth fields
*/
function italicizeMe(x) {
    try {
        var me = document.getElementById(x).textContent;
        if ((me == "Empty") || (me == "CLOSED")) {
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

fetchBooths()