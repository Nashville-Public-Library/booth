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

schedule()
setInterval(schedule, 900000)