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
        let metadata_updated = icecast.metadata_updated
        document.getElementById("metadata_updated").innerText = metadata_updated
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
    document.getElementById("9").innerText = `09am: 1: ${responseJSON[9].booth1} 2: ${responseJSON[9].booth2} 3: ${responseJSON[9].booth3}`;
    document.getElementById("10").innerText = `10am: 1: ${responseJSON[10].booth1} 2: ${responseJSON[10].booth2} 3: ${responseJSON[10].booth3}`;
    document.getElementById("11").innerText = `11am: 1: ${responseJSON[11].booth1} 2: ${responseJSON[11].booth2} 3: ${responseJSON[11].booth3}`;
    document.getElementById("12").innerText = `12pm: 1: ${responseJSON[12].booth1} 2: ${responseJSON[12].booth2} 3: ${responseJSON[12].booth3}`;
    document.getElementById("13").innerText = `01pm: 1: ${responseJSON[13].booth1} 2: ${responseJSON[13].booth2} 3: ${responseJSON[13].booth3}`;
    document.getElementById("14").innerText = `02pm: 1: ${responseJSON[14].booth1} 2: ${responseJSON[14].booth2} 3: ${responseJSON[14].booth3}`;
    document.getElementById("15").innerText = `03pm: 1: ${responseJSON[15].booth1} 2: ${responseJSON[15].booth2} 3: ${responseJSON[15].booth3}`;

}

 function meters (audioElement, meterElement) {
    var audio = audioElement;
    var meter = meterElement;
    var meterWidth = 900; // Adjust meter width as needed

    // Function to update the meter
    function updateMeter(analyser) {
        var dataArray = new Uint8Array(analyser.frequencyBinCount);
        analyser.getByteFrequencyData(dataArray);
        
        // Calculate average amplitude
        var sum = dataArray.reduce((a, b) => a + b, 0);
        var average = sum / dataArray.length;

        // Update meter display
        meter.style.width = (average / 255 * meterWidth) + 'px';

        requestAnimationFrame(function() {
            updateMeter(analyser);
        });
    }

    // Function to create AudioContext and start audio playback
    function startAudio() {
        var audioContext = new (window.AudioContext || window.webkitAudioContext)();
        var analyser = audioContext.createAnalyser();
        var source = audioContext.createMediaElementSource(audio);

        // Connect the audio element to the analyser
        source.connect(analyser);
        analyser.connect(audioContext.destination);

        // Start updating the meter
        updateMeter(analyser);
    }

   startAudio()
}

function meterButton() {
    let live = document.getElementById("audio-live");
    let liveMeter = document.getElementById("audio-live-meter");
    liveMeter.classList.add("meter")
    if (live.paused) {
        live.play();
        meters(audioElement=live, meterElement=liveMeter);
    }
    else {
        live.pause()
    }

    let wpln = document.getElementById("audio-wpln");
    let wplnMeter = document.getElementById("audio-wpln-meter");
    wplnMeter.classList.add("meter")
    if (wpln.paused) {
        wpln.play();
        meters(audioElement=wpln, meterElement=wplnMeter);
    }
    else {
        wpln.pause()
    }

    let fallback = document.getElementById("audio-fallback");
    let fallbackMeter = document.getElementById("audio-fallback-meter")
    fallbackMeter.classList.add("meter")
    if (fallback.paused) {
        fallback.play()
        meters(audioElement=fallback, meterElement=fallbackMeter)
    }
    else {
        fallback.pause()
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
schedule()
setInterval(schedule, 900000)