from flask import render_template

from app import app

# do something to explicitly handle HTTP errors so we don't get some general nginx page

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e), 404

@app.errorhandler(500)
def handle_exception(e):
    return render_template("broken.html", e=e), 500