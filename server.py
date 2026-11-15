"""Serve the Emotion Detector interface and Watson-backed analysis route."""

import requests
from flask import Flask, render_template, request

from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route("/")
def index():
    """Render the application's text entry page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def detect_emotion():
    """Analyze supplied text and format the result for the web interface."""
    text = request.args.get("textToAnalyze", "")
    try:
        result = emotion_detector(text)
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
        app.logger.exception("Watson emotion analysis failed")
        return "Emotion service unavailable. Please try again later.", 503
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!"
    return (
        f"For the given statement, the system response is 'anger': "
        f"{result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. The dominant emotion is "
        f"{result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
