from flask import render_template, request, session, redirect
from twilio.twiml.messaging_response import MessagingResponse

from app import app
from app.auth import check_auth

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    next_url = request.args.get("next")
    print(next_url)
    return render_template("login.html", next_url=next_url)

@app.route("/login/auth", methods=["POST"])
def login_auth():
    req: dict = request.json
    username: str = req.get("username")
    password: str = req.get("password")
    if (check_auth(username=username, password=password)):
        session["logged_in"] = True
        return {"response": "OK"}
    return {"response": "bad login"}, 401

@app.route('/health', methods=['GET', 'POST'])
def health_check():
    return "<div style='font-size: 85pt; text-align: center;'>I AM WORKING FINE</div>" 

@app.route('/twilio', methods=['post'])
def twilio_response():
    resp = MessagingResponse()
    resp.message("Messages sent to this number are not monitored. Please contact Ben directly if you need something.")

    return str(resp)

# do something to explicitly handle HTTP errors so we don't get some general nginx page

@app.errorhandler(400)
def bad_request(e):
    return "you're no good, you're no good", 400

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(405)
def not_allowed(e):
    return "you're no good, you're no good", 405

@app.errorhandler(500)
def handle_exception(e):
    return render_template("broken.html"), 500