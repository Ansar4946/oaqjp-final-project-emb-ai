"""Record real command outputs; pass --live from the Skills Network lab."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"
EVIDENCE.mkdir(exist_ok=True)


def record(filename, arguments):
    """Save a command, its complete output, and its actual exit status."""
    command = [sys.executable, *arguments]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    report = (
        "$ python " + " ".join(arguments) + "\n\n"
        + result.stdout + result.stderr + f"\nExit code: {result.returncode}\n"
    )
    (EVIDENCE / filename).write_text(report, encoding="utf-8")
    print(report)


record("4b_package_validation.txt", ["-c", (
    "import EmotionDetection; "
    "from EmotionDetection import emotion_detector; "
    "print('Package:', EmotionDetection.__file__); "
    "print('Callable:', callable(emotion_detector)); "
    "print('Blank-input contract:', emotion_detector(''))"
)])
record("5b_unit_tests.txt", [
    "-m", "unittest", "-v",
    "test_emotion_detection.TestEmotionDetector",
    "test_emotion_detection.TestWebApplication",
])
record("8b_static_analysis.txt", ["-m", "pylint", "--persistent=n", "server.py"])
if "--live" in sys.argv or "--probe-only" in sys.argv:
    record("2b_3b_live_output.txt", ["-c", (
        "from EmotionDetection import emotion_detector; "
        "print(emotion_detector('I love this new technology.'))"
    )])
if "--live" in sys.argv:
    record("5b_live_tests.txt", ["-c", (
        "import os, unittest; os.environ['RUN_WATSON_TESTS'] = '1'; "
        "suite = unittest.defaultTestLoader.loadTestsFromName("
        "'test_emotion_detection.TestLiveWatson'); "
        "result = unittest.TextTestRunner(verbosity=2).run(suite); "
        "raise SystemExit(not result.wasSuccessful())"
    )])
