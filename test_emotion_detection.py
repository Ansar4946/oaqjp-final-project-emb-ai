"""Contract tests isolated from Watson; optional live rubric examples."""

import os
import unittest
from unittest.mock import Mock, patch

import requests

from EmotionDetection import emotion_detector
from server import app

EXAMPLES = (
    ("I am glad this happened", "joy"),
    ("I am really mad about this", "anger"),
    ("I feel disgusted just hearing about this", "disgust"),
    ("I am so sad about this", "sadness"),
    ("I am really afraid that this will happen", "fear"),
)


class TestEmotionDetector(unittest.TestCase):
    """Verify the real function's request, formatting, and failure behavior."""

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_all_dominant_emotions(self, post):
        """Exercise the five rubric examples against controlled API responses."""
        for text, expected in EXAMPLES:
            with self.subTest(emotion=expected):
                scores = dict.fromkeys(("anger", "disgust", "fear", "joy", "sadness"), 0.01)
                scores[expected] = 0.96
                post.return_value = Mock(status_code=200)
                post.return_value.json.return_value = {
                    "emotionPredictions": [{"emotion": scores}]
                }
                self.assertEqual(emotion_detector(text), {
                    **scores, "dominant_emotion": expected
                })
                self.assertEqual(post.call_args.kwargs["json"], {
                    "raw_document": {"text": text}
                })

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400(self, post):
        """Watson rejects invalid text with six null values."""
        post.return_value = Mock(status_code=400)
        result = emotion_detector("invalid")
        self.assertEqual(len(result), 6)
        self.assertTrue(all(value is None for value in result.values()))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_blank_input(self, post):
        """Blank input is rejected before making a network request."""
        for text in ("", "   ", None):
            self.assertIsNone(emotion_detector(text)["dominant_emotion"])
        post.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_transport_failure(self, post):
        """An outage must never become a fabricated prediction."""
        post.side_effect = requests.Timeout("timeout")
        with self.assertRaises(requests.Timeout):
            emotion_detector("hello")


class TestWebApplication(unittest.TestCase):
    """Exercise the actual Flask routes."""

    def test_index(self):
        """The interface loads successfully."""
        self.assertEqual(app.test_client().get("/").status_code, 200)

    def test_blank_input(self):
        """Missing and whitespace-only input display the rubric error."""
        for text in ("", "   "):
            response = app.test_client().get(
                "/emotionDetector", query_string={"textToAnalyze": text}
            )
            self.assertEqual(response.text, "Invalid text! Please try again!")

    @patch("server.emotion_detector")
    def test_formatted_result(self, detector):
        """The successful route includes the scores and dominant emotion."""
        detector.return_value = dict.fromkeys(
            ("anger", "disgust", "fear", "joy", "sadness"), 0.1
        )
        detector.return_value["dominant_emotion"] = "joy"
        response = app.test_client().get(
            "/emotionDetector", query_string={"textToAnalyze": "I love this"}
        )
        self.assertIn("The dominant emotion is joy.", response.text)

    @patch("server.emotion_detector", side_effect=requests.Timeout("timeout"))
    def test_service_unavailable(self, _detector):
        """A service outage is reported as HTTP 503."""
        with self.assertLogs(app.logger, level="ERROR"):
            response = app.test_client().get(
                "/emotionDetector", query_string={"textToAnalyze": "Hello"}
            )
        self.assertEqual(response.status_code, 503)
        self.assertIn("service unavailable", response.text)


@unittest.skipUnless(os.environ.get("RUN_WATSON_TESTS") == "1", "Live Watson opt-in")
class TestLiveWatson(unittest.TestCase):
    """Run the five assignment assertions against the real Watson model."""

    def test_required_examples(self):
        """Check semantic predictions without mocking the service."""
        for text, expected in EXAMPLES:
            with self.subTest(text=text):
                self.assertEqual(emotion_detector(text)["dominant_emotion"], expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
