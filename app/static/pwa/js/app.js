if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js').then(reg => {
    console.log('[SW] Registered with scope:', reg.scope);

    // Always check for an update when the page becomes visible
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'visible') {
        reg.update(); // 🔄 Triggers update check on visibility
      }
    });

    // Prompt the user when there's a waiting SW
    function promptUserToUpdate(sw) {
      const wantsUpdate = confirm("A new version of the app is available. Do you want to update now?");
      if (wantsUpdate) {
        sw.addEventListener('statechange', () => {
          if (sw.state === 'activated') {
            window.location.reload(); // ✅ Reload only after new SW takes control
          }
        });
        sw.postMessage({ action: 'skipWaiting' }); // 🪄 Activates new SW
      }
    }

    // Handle case where a new SW is already waiting
    if (reg.waiting) {
      promptUserToUpdate(reg.waiting);
    }

    // Handle update found while app is running
    reg.addEventListener('updatefound', () => {
      const newSW = reg.installing;
      newSW.addEventListener('statechange', () => {
        if (newSW.state === 'installed' && navigator.serviceWorker.controller) {
          promptUserToUpdate(newSW); // only prompt if old SW is controlling
        }
      });
    });

    // 🔥 Don't reload blindly on controllerchange — user decides!
  }).catch(err => {
    console.error('[SW] Registration failed:', err);
  });
}



const routes = {
    '/': '/static/pwa/pages/home.html',
    '/schedule': '/static/pwa/pages/schedule.html',
    '/podcasts': '/static/pwa/pages/podcasts.html',
    '/broadcast-schedule': '/static/pwa/pages/broadcastSchedule.html',
    '/program-guide': '/static/pwa/pages/programGuide.html'
  };
  
  async function loadRoute() {
    const path = location.hash.slice(1) || '/';
    const route = routes[path];
  
    const app = document.getElementById('app');
    if (route) {
      const res = await fetch(route);
      const html = await res.text();
      app.innerHTML = html;
    } else {
      app.innerHTML = '<h1>Something went wrong. Not Found.</h1>';
    }

    const viewportMeta = document.getElementById("viewportMeta");
    if (path === '/program-guide' || path === '/broadcast-schedule') {
      viewportMeta.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes');
    } else {
      viewportMeta.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
    }

    if (path === "/podcasts") {
      getArrayOfPodcasts()
    }
  }
  
  window.addEventListener('hashchange', loadRoute);
  window.addEventListener('DOMContentLoaded', loadRoute);
  

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
            updatePlayerMetadata(notAvailable);
            return notAvailable;
        }
        else {
            titleElement.innerText = nowPlaying;
            updatePlayerMetadata(nowPlaying);
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
        { src: '/static/img/NTL_new-192.png', sizes: '192x192', type: 'image/png' },
        { src: '/static/img/NTL_new-512.png', sizes: '512x512', type: 'image/png' }
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

function onlineOffline() {
    if (!navigator.onLine) {
        alert("You are not connected to the internet. The stream and other features will not work until you are back online.");
    } 
}
window.addEventListener('online', onlineOffline); // write something later that alerts the user you are back online, but don't bug them! Don't use an alert().
window.addEventListener('offline', onlineOffline);

// Optionally check on load
onlineOffline();

async function getArrayOfPodcasts() {
    if (!navigator.onLine) {
      document.getElementById("podcastsOffline").style.display = "block"
    }
    const podcastContainer = document.getElementById("podcastsContainer");
    podcastContainer.classList.add("podcastsContainer")
    const url = "/pwa/podcasts";
    try {
      let response = await fetch(url, { method: "POST" });
      let responseJSON = await response.json();
      let podcasts = responseJSON.podcasts
      for (podcast of podcasts) {
        let outer = document.createElement("div");
        outer.style.display = "flex"
        outer.style.width = "100%"
        outer.style.alignItems = "center"
        let podcastInfo = await getPodcastInfo(podcast);
        console.log(podcastInfo.image)
        outer.appendChild(createImageElement(podcastInfo.image, podcastInfo.feed));
        outer.appendChild(createAnchorElement(podcastInfo.feed, podcast));
        podcastContainer.appendChild(outer);
      }
      document.getElementById("podcastSpacer").remove()
      document.getElementById("podcastsContainer").style.overflow = "auto"
    } catch (e) {
      console.error("Failed to load podcasts:", e);
    }
  }

async function getPodcastInfo(podcast) {
  const url = "/pwa/podcasts/info/" + podcast;
  let response = await fetch(url, { method: "POST" });
  let responseJSON = await response.json()
  return responseJSON
}

function createTextNodeInsideDiv(element) {
    let outer = document.createElement("div");
    let inner = document.createTextNode(element)
    outer.style.display = "inline-block"
    outer.style.marginLeft = "10px"
    outer.append(inner);
    return outer;
}

function createImageElement(image, text) {
  let a = document.createElement("a");
  a.href = text
  let img = new Image(130, 130)
  img.style.display = "inline-block"
  img.src = image;
  a.appendChild(img);
  return a;
}

function createAnchorElement(href, text) {
  let a = document.createElement("a");
  a.href = href;
  a.textContent = text;
  a.style.display = "inline-block";
  a.style.marginLeft = "10px";
  a.style.fontSize = "20pt"
  return a;
}