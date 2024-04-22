async function ping() {
    const url = "/status/ping";
          let response = await fetch(url, {method: "POST"});
          let responseJSON = await response.json();

          redGreen(responseJSON.icecast, 'icecast');
          redGreen(responseJSON.wpln, 'wpln');
          redGreen(responseJSON.SGmetadata, 'SGmetadata');
          redGreen(responseJSON.metro, 'metro')
          }

function redGreen(responseIsTrue, id) {
    element = document.getElementById(id)
    if (responseIsTrue) {
        element.style.color = 'green'
    }
    else {
        element.style.color = 'red'
    }
}

async function mountpoints() {
    const url = "/status/stream";
    let response = await fetch(url, {method: "POST"});
    let responseJSON = await response.json();
    let mounts = responseJSON.mounts;
    mountpointElement = document.getElementById('mountpoints');
    mountpointElement.innerText = ''

    mounts.forEach(mount => {
        let newElement = document.createElement("div");
        let newContent = document.createTextNode(mount);
        newElement.appendChild(newContent);
        mountpointElement.appendChild(newElement)
    });
}

async function listeners() {
    const url = "/status/stream";
    let response = await fetch(url, {method: "POST"});
    let responseJSON = await response.json();

    const listenerElement = document.getElementById('listenerCount');
    listenerElement.innerText = responseJSON.listeners
}

async function nowPlaying() {
    let titleElement = document.getElementById('nowPlaying');
    let notAvailable = "Program Name Not Available";
    try {
        const url = "/stream/status";
        let response = await fetch(url, {method: "POST"});
        let icecast = await response.json();
        let nowPlaying = icecast.title;
        if (nowPlaying.trim() == "") {
            titleElement.innerText = notAvailable;
        }
        else {
            titleElement.innerText = nowPlaying;
        }
    }
    catch (whoops) {
        titleElement.innerText = notAvailable;
    }
  }

  async function schedule() {
    const url = "/booth/data";
    let response = await fetch(url, {method: "POST"});
    let responseJSON = await response.json();
    document.getElementById("newspaper").innerText = `Newspaper: ${responseJSON.newspaper}`;
    document.getElementById("9").innerText = `09am: ${responseJSON[9].booth1}, ${responseJSON[9].booth2}, ${responseJSON[9].booth3}`;
    document.getElementById("10").innerText = `10am: ${responseJSON[10].booth1}, ${responseJSON[10].booth2}, ${responseJSON[10].booth3}`;
    document.getElementById("11").innerText = `11am: ${responseJSON[11].booth1}, ${responseJSON[11].booth2}, ${responseJSON[11].booth3}`;
    document.getElementById("12").innerText = `12pm: ${responseJSON[12].booth1}, ${responseJSON[12].booth2}, ${responseJSON[12].booth3}`;
    document.getElementById("13").innerText = `01pm: ${responseJSON[13].booth1}, ${responseJSON[13].booth2}, ${responseJSON[13].booth3}`;
    document.getElementById("14").innerText = `02pm: ${responseJSON[14].booth1}, ${responseJSON[14].booth2}, ${responseJSON[14].booth3}`;
    document.getElementById("15").innerText = `03pm: ${responseJSON[15].booth1}, ${responseJSON[15].booth2}, ${responseJSON[15].booth3}`;

}

function main() {
    ping();
    listeners();
    mountpoints();
    nowPlaying()
}

main()
setInterval(main, 30000)
schedule()
setInterval(schedule, 30000)