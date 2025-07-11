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
      const wantsUpdate = alert("Your app will now be updated to the newest version.");
        sw.addEventListener('statechange', () => {
          if (sw.state === 'activated') {
            window.location.reload(); // ✅ Reload only after new SW takes control
          }
        });
        sw.postMessage({ action: 'skipWaiting' }); // 🪄 Activates new SW
      
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

function fixLayoutGlitch() {
  console.log("fixing layout...");

  const del = document.createElement("div");
  del.style.position = 'absolute';
  del.style.top = '0';
  del.style.left = '0';
  del.style.width = '1px'
  del.style.height = '1px';
  del.style.opacity = '0';
  document.body.appendChild(del)

  requestAnimationFrame(() => {
    del.remove()
    setTimeout(() => {
      window.dispatchEvent(new Event('resize'));
    }, 50);
  });
}

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    fixLayoutGlitch();
  }
});

window.addEventListener('focus', fixLayoutGlitch);




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
      app.innerHTML = '<h1>Something went wrong. Not Found.</h1>';
    }

    // enable zooming for these, which are PDF files
    const viewportMeta = document.getElementById("viewportMeta");
    if (path === '/program-guide' || path === '/broadcast-schedule') {
      viewportMeta.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes');
    } else {
      viewportMeta.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
    }

    // if (path === "/podcasts") {
    //   getArrayOfPodcasts()
    // }
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

async function loadAboutPage() {
  location.hash = "/about"

  const url = "/pwa/version";
  let response = await fetch(url, { method: "POST" });
  let responseJSON = await response.json();
  let version = responseJSON.version;
  document.getElementById("appVersion").innerHTML = "v" + version;
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
