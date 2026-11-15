# Emotion Detector submission guide

## Current status

The official starter was cloned and the application is implemented locally.
Eight isolated unit/web tests pass, package validation passes, and Pylint reports
10.00/10 with exit code 0. Actual terminal output and browser screenshots are in
`evidence/`.

**Not yet ready for a complete submission:** this project has not been published
to your public GitHub repository, and a live Watson request timed out from this
machine. Passing mocked tests establish the client contract, not the accuracy of
the Watson model. Run the live evidence commands in your course lab before
submitting successful-service evidence.

## Rubric mapping

| Item | Submit | Status |
|---|---|---|
| 1 | Your public `README.md` GitHub URL | Publish first |
| 2a | `EmotionDetection/emotion_detection.py` | Implemented |
| 2b | `evidence/2b_3b_live_output.txt` | Current probe fails; rerun in lab |
| 3a | Same detector code, including score dictionary and `max` | Implemented |
| 3b | Successful `evidence/2b_3b_live_output.txt` | Rerun in lab |
| 4a | Your public `EmotionDetection/__init__.py` GitHub URL | Publish first |
| 4b | `evidence/4b_package_validation.txt` | Passed |
| 5a | `test_emotion_detection.py` | Implemented, including five live examples |
| 5b | `evidence/5b_unit_tests.txt`, plus `5b_live_tests.txt` when available | 8 local tests pass; live pending |
| 6a | `server.py` | Implemented |
| 6b | `evidence/6b_deployment_test.png` | Interface captured; replace with live result if required |
| 7a | Detector's `response.status_code == 400` branch | Implemented |
| 7b | Server's `dominant_emotion is None` branch | Implemented |
| 7c | `evidence/7c_error_handling_interface.png` | Captured and visually checked |
| 8a | `server.py` and `python -m pylint --persistent=n server.py` | Implemented/run |
| 8b | `evidence/8b_static_analysis.txt` | 10.00/10, exit 0 |

For task 8, the analysis command runs in a terminal. Do not insert a shell command
into `server.py`; submit the server source and the actual Pylint output.

## Finish live validation

From the project directory in your Skills Network lab:

```bash
python -m pip install -r requirements.txt
python collect_evidence.py --live
```

Check that the live output contains five numeric scores plus `dominant_emotion`,
and the five live example assertions pass. If the course has revised the endpoint,
use the URL supplied by its lab instructions through `WATSON_EMOTION_URL`.
Do not submit a failure log or mocked scores as successful live evidence.

Start `python server.py`; in another terminal install `requirements-evidence.txt`,
run `python -m playwright install chromium`, then
`python capture_screenshots.py --live`. Alternatively, use your browser to analyze
`I love this new technology.`, and save the successful result with the exact
filename `6b_deployment_test.png`. Clear the input, click Analyze emotion, and
save `7c_error_handling_interface.png`.

## Publish your repository

Create an empty **public** repository in your own GitHub account. Do not push
the assignment solution to IBM's starter repository. From this project:

```bash
git remote rename origin upstream
git remote add origin https://github.com/YOUR_USERNAME/emotion-detector.git
git add .
git commit -m "Implement Watson NLP Emotion Detector final project"
git push -u origin main
```

Use your actual username and repository name. If your branch is not `main`, use
the branch shown by `git branch --show-current` for both push and submission URLs.
Verify these URLs load in a signed-out browser:

```text
https://github.com/YOUR_USERNAME/emotion-detector/blob/main/README.md
https://github.com/YOUR_USERNAME/emotion-detector/blob/main/EmotionDetection/__init__.py
```

## Code snippets

Copy the full current contents of each of these files into the relevant answer:

- Tasks 2a, 3a, 7a: `EmotionDetection/emotion_detection.py`.
- Task 5a: `test_emotion_detection.py`.
- Tasks 6a, 7b, 8a: `server.py`.

Use the actual saved outputs and screenshots for the other answers. Review every
answer and upload before selecting Submit assignment yourself.
