/*
output date to top left
*/
function real_date() {
const today = new Date();
const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

let month = months[today.getMonth()];
let day = days[today.getDay()];
let dateNumber = today.getDate();

document.getElementById('date').innerHTML = day + " " + month + " " + dateNumber
}
real_date()
setInterval(real_date, 60000)


/*
output current time to top right
*/
function real_time() {
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

// need a fix for midnight. we don't want to display the time as 00:00. we want 12:00
if (hour == 0) {
  hour = 12
}
var minute = now.getMinutes()
if (minute < 10) {
  minute = '0' + minute
}
var realtime = hour + ':' + minute + ampm

document.getElementById('time').innerHTML = realtime
}
real_time()
setInterval(real_time, 1000)


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
italicizeMe("Booth1_data")
italicizeMe("Booth2_data")
italicizeMe("Booth3_data")
italicizeMe("Booth1_2_data")
italicizeMe("Booth2_2_data")
italicizeMe("Booth3_2_data")