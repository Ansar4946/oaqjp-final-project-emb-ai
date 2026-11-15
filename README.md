# Final project

## Emotion Detector

A Flask web application for the IBM Skills Network Emotion Detector final project.
It sends text to Watson NLP, returns anger, disgust, fear, joy, and sadness scores,
and identifies the dominant emotion.

Starter repository: https://github.com/ibm-developer-skills-network/oaqjp-final-project-emb-ai

## Run locally

Use Python 3.10 or newer. From this directory:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe server.py
```

Open http://127.0.0.1:5000. The Flask development server is for local/course
deployment. The interface has no external stylesheet or script dependency.

If the course environment requires port 5000:

```bash
python -m flask --app server run --host 0.0.0.0 --port 5000
```

## Package usage

```python
from EmotionDetection import emotion_detector
print(emotion_detector("I love this new technology."))
```

The returned dictionary contains `anger`, `disgust`, `fear`, `joy`, `sadness`,
and `dominant_emotion`. Scores come directly from Watson. Blank input and an
HTTP 400 response produce six `None` values. The web route displays
`Invalid text! Please try again!` for these cases. Transport failures and
unexpected responses produce HTTP 503 with a service-unavailable message.

The default service URL is the Skills Network Watson endpoint. Set
`WATSON_EMOTION_URL` before starting Python only if the course supplies a different
endpoint. A timeout was observed from this machine; live prediction has not been
validated here. No fallback model or fabricated score is used.

## Validation and evidence

```powershell
.\.venv\Scripts\python.exe collect_evidence.py
# Run this in an environment with access to the course Watson service:
.\.venv\Scripts\python.exe collect_evidence.py --live
```

The local suite has eight tests, including all five dominant-emotion branches,
the request payload, HTTP 400, blank input, transport failure, and Flask routes.
Controlled API responses isolate the unit tests from network availability.
The separate live test checks all five required sentences against Watson.

`python -m unittest -v` also discovers the live test; it is skipped unless
`RUN_WATSON_TESTS=1`. `collect_evidence.py --live` enables it automatically.

Static analysis: `python -m pylint --persistent=n server.py`.
Recorded result: **10.00/10**, exit code 0, without disabling lint rules.

Screenshots can be recreated while the server runs:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-evidence.txt
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe capture_screenshots.py
# Once Watson works, replace the deployment screenshot with a successful analysis:
.\.venv\Scripts\python.exe capture_screenshots.py --live
```

`--chromium PATH` can use an existing Chromium installation. The current
`6b_deployment_test.png` shows the deployed interface, with no prediction claimed.
`7c_error_handling_interface.png` shows the actual blank-input response.

See [SUBMISSION.md](SUBMISSION.md) for the mapping to all 16 rubric items,
including the steps still required before submitting.
