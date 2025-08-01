const appVersion = "{{version}}";

function openlinkExternalWindow(url) {
  window.open(url, '_blank', 'noopener');
} 

const routes = {
    '/': '/static/pwa/pages/home.html',
    '/about': 'static/pwa/pages/about.html',
    '/schedule': '/static/pwa/pages/schedule.html',
    '/podcasts': '/static/pwa/pages/podcasts.html',
    '/podcasts-individual': '/static/pwa/pages/podcast-loading.html',
    '/broadcast-schedule': '/static/pwa/pages/broadcastSchedule.html',
    '/program-guide': '/static/pwa/pages/programGuide.html',
    '/schedule/monday': '/static/pwa/pages/daily/monday.html',
    '/schedule/tuesday': '/static/pwa/pages/daily/tuesday.html',
    '/schedule/wednesday': '/static/pwa/pages/daily/wednesday.html',
    '/schedule/thursday': '/static/pwa/pages/daily/thursday.html',
    '/schedule/friday': '/static/pwa/pages/daily/friday.html',
    '/schedule/saturday': '/static/pwa/pages/daily/saturday.html',
    '/schedule/sunday': '/static/pwa/pages/daily/sunday.html'
  };
  
  async function loadRoute() {
    const path = location.hash.slice(1) || '/';
    const route = routes[path];
  
    const app = document.getElementById('app');
    app.innerHTML = "<div> </div>"
    await new Promise(requestAnimationFrame);
    if (route) {
      const res = await fetch(route);
      const html = await res.text();
      app.innerHTML = html;
    } else {
      app.innerHTML = "<h1>We're so sorry, but something went wrong. Not Found.</h1>";
    }

    if (path === "/about") {
      loadAppVersion()
    }

    if (path === "/podcasts") {
      loadShowNamesInSearchInput()
      let categorySelected = sessionStorage.getItem("pocastCategory");
      if (categorySelected) {
        let categoryDropdown = document.getElementById("categorySelector");
        categoryDropdown.value = categorySelected
        categorySelector(categorySelected);
      }
    }
  }
  
  window.addEventListener('hashchange', loadRoute);
  window.addEventListener('DOMContentLoaded', loadRoute);
  

  async function nowPlaying() {
    let titleElement = document.getElementById('nowPlaying');
    let livestream = document.getElementById("audio");
    let notAvailable = "Program Name Not Available";
    try {
        const url = "/stream/status";
        let response = await fetch(url, { method: "POST" });
        let icecast = await response.json();
        let nowPlaying = icecast.title;
        if (nowPlaying.trim() == "") {
            titleElement.innerText = notAvailable;
            if (!livestream.paused) {updatePlayerMetadata(notAvailable);}
            return notAvailable;
        }
        else {
            titleElement.innerText = nowPlaying;
            if (!livestream.paused) { updatePlayerMetadata(nowPlaying);}

            return nowPlaying;
        }
    }
    catch (whoops) {
        titleElement.innerText = notAvailable;
        updatePlayerMetadata(notAvailable);
        return notAvailable;
    }
  }
  nowPlaying()
  setInterval(nowPlaying, 30000) // 30 seconds
  

  const button = document.getElementById('playPauseButton');
  button.addEventListener('click', () => {
  const audio = document.getElementById('audio');
    if (audio.paused) {
      if (!navigator.onLine){return;}
      nowPlaying()
      audio.src = "/stream/livestream.mp3"
      audio.play();
      switchPlayPauseIcon()
      button.setAttribute('aria-label', 'Pause');
    } else {
      audio.pause();
      switchPlayPauseIcon()
      button.setAttribute('aria-label', 'Play');
    }
  });

function switchPlayPauseIcon() {
  const playIcon = document.getElementById('playIcon');
  const pauseIcon = document.getElementById('pauseIcon');
  if (playIcon.style.display == "none") {
    pauseIcon.style.display = "none";
    playIcon.style.display = "block"
  } else {
    playIcon.style.display = "none";
    pauseIcon.style.display = "block"
  }
}



function updatePlayerMetadata(nowPlayingTitle) {
  const audio = document.getElementById('audio');
  if ('mediaSession' in navigator) {
    navigator.mediaSession.metadata = new MediaMetadata({
      title: nowPlayingTitle,
      artist: 'Nashville Talking Library',
      album: 'Live Stream',
      artwork: [
        { src: '/static/pwa/img/NTL_new-192.jpg', sizes: '192x192', type: 'image/jpg' },
        { src: '/static/pwa/img/NTL_new-512.jpg', sizes: '512x512', type: 'image/jpg' }
      ]
    });
    // Only expose play/pause, disable seek
    navigator.mediaSession.setActionHandler('play', () => {
      audio.play();
      switchPlayPauseIcon();
    });
    navigator.mediaSession.setActionHandler('pause', () => {
      audio.pause();
      switchPlayPauseIcon();
    });
    ['seekbackward', 'seekforward', 'previoustrack', 'nexttrack']
      .forEach(a => { try { navigator.mediaSession.setActionHandler(a, null); } catch { } });
  }
}

function handleMuteButton() {
  const audio = document.getElementById("audio");
  const muteButton = document.getElementById("muteButton");
  if (audio.paused) {return};
  let volume = audio.volume;
  if (volume === 1) {
    console.log("changing volume to 0.0001");
    audio.volume = 0.0001;
    muteButton.innerText = "UNMUTE"
  } else {
    console.log("changing volume to 1")
    audio.volume = 1
    muteButton.innerText = "MUTE"
  }
  
}

function onlineOffline() {
  const onlineOfflineDotColor = document.getElementById("onlineOfflineDot");
  if (!navigator.onLine) {
    onlineOfflineDotColor.style.backgroundColor = "#f31642";
    alert("You are not connected to the internet. The stream and other features will not work until you are back online.");
  } else {
    onlineOfflineDotColor.style.backgroundColor = "#00fc37";
  }
}
window.addEventListener('online', onlineOffline);
window.addEventListener('offline', onlineOffline);

// check on load
onlineOffline();

function loadAppVersion() {
  document.getElementById("appVersion").innerHTML = "v" + appVersion;
}

  async function loadPodcast(show) {  
    // show the loading page, then go fetch the data from the server and render when ready

    if (!navigator.onLine) {
      alert("You cannot listen to podcasts while offline.");
      return;
    }
    location.hash = "/podcasts-individual"
    const app = document.getElementById("app");

    const url = "/pwa/podcasts/info/" + show;
    let response = await fetch(url, { method: "POST", headers: {'Content-Type': 'text/html'}});
    if (response.ok) {
      let responseHTML = await response.text();
      app.innerHTML = responseHTML
      } else {
        app.innerHTML = "<h1>Sorry, we're having trouble fetching podcasts</h1>"
      }
    }

  function noPodcastWarning (show) {
    alert(`We do not currently offer a podcast for ${show}.`)
  }


document.addEventListener('play', function (e) {
  var audios = document.getElementsByTagName('audio');
  for (var i = 0, len = audios.length; i < len; i++) {
    if (audios[i] != e.target) {
      audios[i].pause();
    }
  }

  if (e.target.id !== "audio") {
    const playIcon = document.getElementById('playIcon');
    const pauseIcon = document.getElementById('pauseIcon');
    playIcon.style.display = "block";
    pauseIcon.style.display = "none";
  }
}, true);

function categorySelector(category) {
  const podcasts = document.getElementsByClassName("podcastIndividual");
  const speed = 250;

  sessionStorage.setItem("pocastCategory", category)

  for (let i = 0; i < podcasts.length; i++) {
    let podcast = podcasts[i];

    // if set to 'all', show all podcasts
    if (category == "all") {
      podcast.style.display = "block";
      setTimeout(() => {
        podcast.style.opacity = '1';
      }, speed);
      continue; // next iteration
    }

    let categories = podcast.dataset.category.split(",");
    if (categories.includes(category)) {
      podcast.style.display = "block";
      setTimeout(() => {
        podcast.style.opacity = '1'
      }, speed);
    } else {
      podcast.style.opacity = "0";
      setTimeout(() => {
        podcast.style.display = "none";
      }, speed);

    }
  }
}

async function podcastSearch(title) {
  const titleTrim = title.trim()
  if (titleTrim == "") {return;}

  const url = "/pwa/podcasts"
  let response = await fetch(url, { method: "POST" });
  let responseJSON = await response.json();
  let show = responseJSON.shows[titleTrim]
  if (show) {
    loadPodcast(show)
  } else {
    alert(`Sorry, we don't have a show called ${titleTrim}. (we can change this message to anything)`)
  }
}

async function loadShowNamesInSearchInput() {
  const datalist = document.getElementById("podcastSearchList");

  const url = "/pwa/podcasts"
  let response = await fetch(url, { method: "POST" });
  let responseJSON = await response.json();
  let shows = responseJSON.shows

  for (const key in shows) {
    const option = document.createElement("option");
    option.value = key;
    datalist.appendChild(option)
  }
}