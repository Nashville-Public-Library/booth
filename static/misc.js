// output date to top left
const today = new Date();
const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

let month = months[today.getMonth()];
let day = days[today.getDay()];
let dateNumber = today.getDate();

document.getElementById('date').innerHTML = day + " " + month + " " + dateNumber

// output current time to top right
function realtime() {
const now = new Date();
var hour = now.getHours()
if (hour == 12) {
  ampm = 'pm'
} else if (hour > 12) {
  hour = hour - 12
  ampm = 'pm'
} else {
  ampm = 'am'
}


var minute = now.getMinutes()
if (minute < 10) {
  minute = '0' + minute
}

var realtime = hour + ':' + minute + ampm

document.getElementById('time').innerHTML = realtime
}
realtime()
setInterval(realtime, 4000) 

// italicize empty/closed booth fields
function italicizeMe(x) {
    var me = document.getElementById(x).textContent;
    if ( (me == "Empty") || (me == "CLOSED") ) {
    document.getElementById(x).style.fontStyle = 'italic';
      }
    }
italicizeMe("Booth1_data")
italicizeMe("Booth2_data")
italicizeMe("Booth3_data")
italicizeMe("Booth1_2_data")
italicizeMe("Booth2_2_data")
italicizeMe("Booth3_2_data")