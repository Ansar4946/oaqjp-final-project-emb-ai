"""Analyze text using the Skills Network Watson NLP emotion service."""

import os

import requests

EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")
SERVICE_URL = os.environ.get(
    "WATSON_EMOTION_URL",
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict",
)


def emotion_detector(text_to_analyse):
    """Return five emotion scores and the dominant emotion; nulls for HTTP 400.

    Transport errors and other unsuccessful statuses propagate to the caller.
    No synthetic predictions are substituted when Watson is unavailable.
    """
    empty_result = dict.fromkeys((*EMOTIONS, "dominant_emotion"))
    if not isinstance(text_to_analyse, str) or not text_to_analyse.strip():
        return empty_result
    response = requests.post(
        SERVICE_URL,
        json={"raw_document": {"text": text_to_analyse}},
        headers={"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"},
        timeout=30,
    )
    if response.status_code == 400:
        return empty_result
    response.raise_for_status()
    scores = response.json()["emotionPredictions"][0]["emotion"]
    result = {emotion: scores[emotion] for emotion in EMOTIONS}
    result["dominant_emotion"] = max(result, key=result.get)
    return result
