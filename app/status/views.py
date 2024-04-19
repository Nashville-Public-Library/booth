from flask import render_template

from app import app

@app.route('/status')
def status():
    return render_template('status.html')