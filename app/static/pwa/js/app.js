const routes = {
    '/': 'static/pwa/pages/home.html',
    '/schedule': 'static/pwa/pages/schedule.html',
    '/podcasts': 'static/pwa/pages/podcasts.html',
    '/broadcast-schedule': 'static/pwa/pages/broadcastSchedule.html',
    '/program-guide': 'static/pwa/pages/programGuide.html'
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
        const url = "https://api.nashvilletalkinglibrary.com/stream/status";
        let response = await fetch(url, { method: "POST" });
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
  nowPlaying()
  setInterval(nowPlaying, 60000) // 1 minute
  

  const button = document.getElementById('playPauseButton');
  const audio = document.getElementById('audio');
  button.addEventListener('click', () => {
  const playIcon = document.getElementById('playIcon');
  const pauseIcon = document.getElementById('pauseIcon');
    if (audio.paused) {
      audio.play();
      playIcon.style.display = 'none';
      pauseIcon.style.display = 'block';
      button.setAttribute('aria-label', 'Pause');
      updateMetadata()
    } else {
      audio.pause();
      playIcon.style.display = 'block';
      pauseIcon.style.display = 'none';
      button.setAttribute('aria-label', 'Play');
    }
  });

  function updateMetadata() {
    if ('mediaSession' in navigator) {
  navigator.mediaSession.metadata = new MediaMetadata({
    title: 'Nashville Talking Library',
    artist: 'Nashville Talking Library',
    album: 'Nashville Talking Library',
    artwork: [
      { src: '/static/img/icon-192.png',   sizes: '192x192',   type: 'image/png' },
      { src: '/static/img/icon-512.png',   sizes: '512x512',   type: 'image/png' }
    ]
  });
}
  navigator.mediaSession.setActionHandler('play', () => audio.play());
  navigator.mediaSession.setActionHandler('pause', () => audio.pause());

  // 3. Disable all seek / track‐change controls:
  ['seekbackward', 'seekforward', 'previoustrack', 'nexttrack', 'stop']
    .forEach(action => {
      try {
        navigator.mediaSession.setActionHandler(action, null);
      } catch (e) {
        // Some browsers may throw if they don't support the action
      }
    });

  }