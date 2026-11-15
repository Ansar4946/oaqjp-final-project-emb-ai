"use strict";

document.getElementById("analysis-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const output = document.getElementById("system_response");
    const button = document.getElementById("analyze-button");
    const query = new URLSearchParams({
        textToAnalyze: document.getElementById("textToAnalyze").value
    });
    button.disabled = true;
    output.textContent = "Analyzing...";
    try {
        const response = await fetch(`/emotionDetector?${query}`);
        output.textContent = await response.text();
    } catch (error) {
        output.textContent = "Unable to reach the application. Please try again.";
    } finally {
        button.disabled = false;
    }
});
