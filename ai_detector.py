# ai_detector.py

def ai_detect(input_data: str):
    """
    AI detection disabled for Hugging Face deployment
    (Ollama not supported in container environment)
    """

    return {
        "attack": "Unknown",
        "severity": "LOW",
        "confidence": 0.3,
        "explanation": "AI disabled in deployment (Ollama not supported)"
    }