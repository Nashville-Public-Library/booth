async function fetchPost(fetchURL, fetchOptions=null) {
    let response = await fetch(fetchURL, fetchOptions);
    let responseJSON = await response.json();
    return responseJSON;
}

async function ping() {
    /* 
    Get all the child elements of the ping element. Loop through them all, 
    and send their id to the server. On the server, the ids are matched to the IP/hostnames 
    we want to ping.
    */
    const pingElements = document.getElementById("ping").children;
    for (el of pingElements){
        el = el.id;
        const pendingColor = document.getElementById("ping").style.color // so we only have to set the pending color once
        document.getElementById(el).style.color = pendingColor;
        
        const url = "/status/ping";
        const options = {
            headers: {'Accept': 'application/json','Content-Type': 'application/json'},
            method: "POST", 
            body: JSON.stringify({"host": el})
            }
        let response = await fetchPost(fetchURL=url, fetchOptions=options);
        
        result = response.result;
        redGreen(responseIsTrue=result, id=el);
    }
    }

function redGreen(responseIsTrue, id) {
    element = document.getElementById(id);
    if (responseIsTrue) {
        element.style.color = 'green';
    }
    else {
        element.style.color = 'red';
    }
}

async function fetchUserAgent(mount) {
    mount = mount.replace("/", "");
    const url = '/status/useragent';

    const options = {
        headers: {'Accept': 'application/json','Content-Type': 'application/json'},
        method: "POST",
        body: JSON.stringify({"mount": mount})
        }
    let response = await fetchPost(fetchURL=url, fetchOptions=options);
    return response.userAgent;
}

// pass in the text node you want to create. the TEXT/CONTENT of the element
function createTextNodeInsideDiv(element) {
    let outer = document.createElement("div");
    let inner = document.createTextNode(element)
    outer.append(inner);
    return outer;
}

async function userAgent() {
    const url = "/status/mounts";
    const options = { method: "POST" }
    let response = await fetchPost(fetchURL=url, fetchOptions=options);

    const userAgentElement = document.getElementById('userAgent');
    userAgentElement.innerHTML = ""

    let mounts = response.mountList;
    for (mount of mounts) {
        let outerElement = createTextNodeInsideDiv(mount);
        outerElement.classList.add("border")

        const mountpointArray = await fetchUserAgent(mount);
        mountpointArray.forEach(mountpoint => {
            let innerElement = createTextNodeInsideDiv(mountpoint)
            outerElement.appendChild(innerElement)
        })
        userAgentElement.appendChild(outerElement)
    }
}

async function mountpoints() {
    // yeah this isn't a mess AT ALL
    const url = "/status/stream";
    const options = {method: "POST"}
    let response = await fetchPost(fetchURL=url, fetchOptions=options);

    document.getElementById('listenerCount').innerHTML = response.listeners;
    document.getElementById("serverStart").innerText = response.serverStart;
    document.getElementById('outgoing_kbitrate').innerText = `${response.outgoing_kbitrate}kbps`;
    document.getElementById("sources").innerText = response.sources;

    const mountpointElement = document.getElementById('mountpoints');
    mountpointElement.innerHTML = ''
    let mounts = response.mounts;
    for (mount of mounts) {
        
        let containerElement = document.createElement("div");
        containerElement.classList.add("border");

        containerElement.appendChild(createTextNodeInsideDiv(`Name: ${mount['name']}`));
        containerElement.appendChild(createTextNodeInsideDiv(`Stream Start: ${mount['stream_start']}`));
        containerElement.appendChild(createTextNodeInsideDiv(`Listeners: ${mount['listeners']}`));
        containerElement.appendChild(createTextNodeInsideDiv(`Incoming Bitrate: ${mount['incoming_bitrate']}kbps`));
        containerElement.appendChild(createTextNodeInsideDiv(`Outgoing Bitrate: ${mount['outgoing_kbitrate']}kbps`));
        containerElement.appendChild(createTextNodeInsideDiv(`Title: ${mount['title']}`));
        containerElement.appendChild(createTextNodeInsideDiv(`Metadata Updated: ${mount['metadata_updated']}`));

        mountpointElement.appendChild(containerElement);
    };
}

async function audioElements() {
    const url = "/status/stream";
    const options = {method: "POST"}
    let response = await fetchPost(fetchURL=url, fetchOptions=options);

    const AudioElement = document.getElementById('audio');
    let mounts = response.mounts;
    for (mount of mounts) {
        let containerElement = document.createElement("div");
        let audio = new Audio(mount['listenurl']);
        audio.controls = true;
        audio.preload = "none";
        containerElement.appendChild(createTextNodeInsideDiv(mount['name']))
        containerElement.appendChild(audio);

        AudioElement.appendChild(containerElement)
    }
}

  async function schedule() {

    document.getElementById("dots").style.display = 'block'
    const url = "/booth/data";
    const options = {method: "POST"}
    let response = await fetchPost(fetchURL=url, fetchOptions=options);


    document.getElementById("newspaper").innerText = `Newspaper: ${response.newspaper}`;
    document.getElementById("9").innerText = `09am: 1: ${response[9].booth1} 2: ${response[9].booth2} 3: ${response[9].booth3}`;
    document.getElementById("10").innerText = `10am: 1: ${response[10].booth1} 2: ${response[10].booth2} 3: ${response[10].booth3}`;
    document.getElementById("11").innerText = `11am: 1: ${response[11].booth1} 2: ${response[11].booth2} 3: ${response[11].booth3}`;
    document.getElementById("12").innerText = `12pm: 1: ${response[12].booth1} 2: ${response[12].booth2} 3: ${response[12].booth3}`;
    document.getElementById("13").innerText = `01pm: 1: ${response[13].booth1} 2: ${response[13].booth2} 3: ${response[13].booth3}`;
    document.getElementById("14").innerText = `02pm: 1: ${response[14].booth1} 2: ${response[14].booth2} 3: ${response[14].booth3}`;
    document.getElementById("15").innerText = `03pm: 1: ${response[15].booth1} 2: ${response[15].booth2} 3: ${response[15].booth3}`;

    // remove loading indicator 'dots' CSS from element
    document.getElementById("dots").style.display = 'none'
}

async function banner() {
    const url = "/booth/banner/content";
    const options = {method: "POST"}
    let response = await fetchPost(fetchURL=url, fetchOptions=options);

    const banner = response.banner
    const bannerElement = document.getElementById("banner");
    if (banner) {
        bannerElement.innerText = banner
    }
    else {
        bannerElement.innerText = 'none'
    }

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

function check_time() {
    const current_time = new Date()
    var minute = current_time.getMinutes()
    const updateTimes = [0, 30];
    if (updateTimes.includes(minute)) {
        schedule();
    }
}

function main() {
    mountpoints();
    userAgent();
    banner();
    ping();
}

main()
setInterval(main, 120000)
audioElements()
schedule()
setInterval(check_time, 60000)