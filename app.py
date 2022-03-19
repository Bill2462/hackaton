from flask import Flask, render_template, request
from intent_detection import Detector
from process import process_request
from display import display_result

app = Flask(__name__)
intent_detector = None
preference_detector = None

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        req = request.form["request"]
        address = request.form["where"]
        preferences = request.form["preferences"]
        result = process_request(intent_detector, preference_detector, req, preferences, address)
        return display_result(result, request)

    return render_template("page.html")

if __name__ == "__main__":
    print("Loading intent model ...")
    intent_detector = Detector("intents.pkl")

    print("Loading preferences model ...")
    preference_detector = Detector("prefs.pkl")
    app.run()
