async function fetchBooths() {
    const booth1_1_display = document.getElementById('Booth1_data');
    const booth2_1_display = document.getElementById('Booth2_data');
    const booth3_1_display = document.getElementById('Booth3_data');
    const booth1_2_display = document.getElementById('Booth1_2_data');
    const booth2_2_display = document.getElementById('Booth2_2_data');
    const booth3_2_display = document.getElementById('Booth3_2_data');
    try {
        var url = "/booth/data"
        var response = await fetch(url);
        var responseJSON = await response.json()

        let dots = document.querySelectorAll('.dot-elastic');
        for (let i = 0; i < dots.length; i++) {
            dots[i].classList.remove('dot-elastic')
        }

        booth1_1_display.innerText = responseJSON.booth1_1;
        booth2_1_display.innerText = responseJSON.booth2_1;
        booth3_1_display.innerText = responseJSON.booth3_1;
        booth1_2_display.innerText = responseJSON.booth1_2;
        booth2_2_display.innerText = responseJSON.booth2_2;
        booth3_2_display.innerText = responseJSON.booth3_2;

        italicizeMe("Booth1_data")
        italicizeMe("Booth2_data")
        italicizeMe("Booth3_data")
        italicizeMe("Booth1_2_data")
        italicizeMe("Booth2_2_data")
        italicizeMe("Booth3_2_data")
    }
    catch (err) {
        console.log(err)
    }
}

/*
italicize empty/closed booth fields
*/
function italicizeMe(x) {
    try {
        var me = document.getElementById(x).textContent;
        if ((me == "Empty") || (me == "CLOSED")) {
            document.getElementById(x).style.fontStyle = 'italic';
        }
    }
    catch {
        console.log('oh well')
    }
}

fetchBooths()