//output date to top of screen
const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const m = new Date();
let month = months[m.getMonth()];

const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const d = new Date();
let day = days[d.getDay()];
let dateNumber = d.getDate()

document.getElementById('date').innerHTML = day + " " + month + " " + dateNumber

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