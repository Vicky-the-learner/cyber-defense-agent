import os
import urllib.request
import json

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://kiko555-cyber-defense-agent.hf.space"
)

if not API_BASE_URL:
    print("ERROR: API_BASE_URL not set")
    exit(1)

TASKS = ["easy", "medium", "hard"]
