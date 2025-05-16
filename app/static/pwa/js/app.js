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
            return notAvailable;
        }
        else {
            titleElement.innerText = nowPlaying;
            return nowPlaying;
        }
    }
    catch (whoops) {
        titleElement.innerText = notAvailable;
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

audio.addEventListener('play', async () => {
  const audio = document.getElementById('audio');
  let nowPlayingTitle = await nowPlaying()
  if ('mediaSession' in navigator) {
    navigator.mediaSession.metadata = new MediaMetadata({
      title: nowPlayingTitle,
      artist: 'Nashville Talking Library',
      album:  'Live Stream',
      artwork: [
        { src: '/static/img/NTL_new-192.png', sizes: '192x192', type: 'image/png' },
        { src: '/static/img/NTL_new-512.png', sizes: '512x512', type: 'image/png' }
      ]
    });
    console.log(navigator.mediaSession.metadata)

    // Only expose play/pause, disable seek
    navigator.mediaSession.setActionHandler('play',  () => audio.play());
    navigator.mediaSession.setActionHandler('pause', () => audio.pause());
    ['seekbackward','seekforward','previoustrack','nexttrack','stop']
      .forEach(a => { try { navigator.mediaSession.setActionHandler(a, null); } catch {} });
  }
});