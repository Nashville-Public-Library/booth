async function detect() {
    const hover = window.matchMedia('(hover: hover)').matches;
    if (hover) {
        document.body.innerHTML = "<div style='text-align: center; margin-top: 20%; font-size: 50pt;'>ONLY AVAILABLE ON MOBILE</div>";
        return;
    }

    const installed = window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;
    // const installed = true;
    if (!installed) {
        console.log('not installed, fetching page');
        let response = await fetch('/static/pwa/pages/install.html');
        let text = await response.text()

        document.body.innerHTML = text;
    }
}

detect()