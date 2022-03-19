from flask import Flask, render_template, request
from intent_detection import Detector

app = Flask(__name__)
intent_detector = None

@app.route("/")
def home():
    return render_template("page.html")

@app.route("/process", methods=["POST"])
def process():
    text = request.form["text"]
    detected = intent_detector(text)
    return next(iter(detected))[0]

if __name__ == "__main__":
    intent_detector = Detector("intents.pkl")
    app.run()
