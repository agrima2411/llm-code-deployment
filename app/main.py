# app/main.py

import json
from typing import Dict

# ====== Configuration ======
# Your secret (must match what you submit in the Google Form)
API_SECRET = "This-is-my-secret."

# ====== Helper Functions ======

def verify_secret(request_secret: str) -> bool:
    """
    Verify that the secret sent in the request matches your API secret.
    """
    return request_secret == API_SECRET


def parse_request(request_body: Dict) -> Dict:
    """
    Validate and parse the incoming request JSON.
    Returns a dictionary with required fields.
    """
    required_fields = ["email", "secret", "task", "round", "nonce", "brief"]
    parsed = {field: request_body.get(field) for field in required_fields}
    return parsed


def build_evaluation_payload(request_data: Dict, repo_url: str = "", commit_sha: str = "", pages_url: str = "") -> Dict:
    """
    Prepare the JSON payload to send back to the evaluation API.
    """
    payload = {
        "email": request_data.get("email"),
        "task": request_data.get("task"),
        "round": request_data.get("round"),
        "nonce": request_data.get("nonce"),
        "repo_url": repo_url,
        "commit_sha": commit_sha,
        "pages_url": pages_url
    }
    return payload


def generate_repo_code(task_id: str) -> str:
    """
    Placeholder function where you would generate code using LLM.
    Returns a string representing the main code content.
    """
    return f"# This is generated code for task {task_id}\nprint('Hello from task {task_id}')"


def send_to_evaluation(payload: Dict, evaluation_url: str) -> Dict:
    """
    Placeholder for sending payload to the evaluation API.
    Currently returns payload for testing.
    """
    # In real usage, you would use:
    # import requests
    # response = requests.post(evaluation_url, json=payload)
    # return response.json()
    return payload
