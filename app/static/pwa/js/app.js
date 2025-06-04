if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js').then(reg => {
    console.log('[SW] Registered with scope:', reg.scope);

    // Example update detection logic
    reg.onupdatefound = () => {
      const newWorker = reg.installing;
      newWorker.onstatechange = () => {
        if (newWorker.state === 'installed') {
          if (navigator.serviceWorker.controller) {
            // There is a new version available
            if (confirm("A new version of the app is available. Do you want to update now?")) {
              window.location.reload();
            }
          }
        }
      };
    };
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
  setInterval(nowPlaying, 60000) // 1 minute
  

  const button = document.getElementById('playPauseButton');
  button.addEventListener('click', () => {
  const audio = document.getElementById('audio');
  const playIcon = document.getElementById('playIcon');
  const pauseIcon = document.getElementById('pauseIcon');
    if (audio.paused) {
      if (!navigator.onLine){return;}
      nowPlaying()
      audio.src = "/stream/livestream.mp3"
      audio.play();
      playIcon.style.display = 'none';
      pauseIcon.style.display = 'block';
      button.setAttribute('aria-label', 'Pause');
    } else {
      audio.pause();
      pauseIcon.style.display = 'none';
      playIcon.style.display = 'block';
      button.setAttribute('aria-label', 'Play');
    }
  });

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
    navigator.mediaSession.setActionHandler('play', () => audio.play());
    navigator.mediaSession.setActionHandler('pause', () => audio.pause());
    ['seekbackward', 'seekforward', 'previoustrack', 'nexttrack', 'stop']
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
