async function ping() {
    const url = "/status/ping";
          let response = await fetch(url, {method: "POST"});
          let responseJSON = await response.json();

          redGreen(responseJSON.streamGuys, 'streamGuys');
          redGreen(responseJSON.wpln, 'wpln');
          redGreen(responseJSON.SGmetadata, 'SGmetadata');
          redGreen(responseJSON.metro, 'metro')
          }

function redGreen(responseIsTrue, id) {
    element = document.getElementById(id)
    if (responseIsTrue) {
        element.classList.add('statusGreen')
    }
    else {
        element.classList.add('statusRed')
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
        newElement.classList.add('statusGreen')
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

function main() {
    ping();
    listeners();
    mountpoints();
    nowPlaying()
}

main()
setInterval(main, 30000)
