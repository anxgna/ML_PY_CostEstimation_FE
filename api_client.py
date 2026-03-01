import httpx
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def post_predict(payload):
    return httpx.post(f"{API_BASE_URL}/predict", json=payload)

def get_predictions():
    return httpx.get(f"{API_BASE_URL}/predictions")
