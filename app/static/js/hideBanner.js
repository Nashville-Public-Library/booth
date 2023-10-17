/*
If banner element is on the page, remove footer/images BUT only for BrightSign, 
which we target below. We blew up the font for BrightSign so big (staff request) that
we can't fit everything on the screen.
 
This feels hacky, sorry.
*/

window.onload = hide_footer()

function hide_footer() {
    is_BrightSign = window.navigator.userAgent.includes('Bright');

    if (is_BrightSign) {
        document.getElementById('footer').style.visibility = 'hidden';
    }
}