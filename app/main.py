from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

app = FastAPI()

@app.post("/github/repo")
async def create_repo(request: Request):
    """
    Creates a new GitHub repository for the task.
    Expected input JSON: {"repo_name": "captcha-solver-123"}
    """
    data = await request.json()
    repo_name = data.get("repo_name")

    if not repo_name:
        return {"error": "Missing repo_name"}

    # GitHub API endpoint
    url = "https://api.github.com/user/repos"

    # Payload for creating a repository
    payload = {
        "name": repo_name,
        "description": "Auto-created repo for LLM Deployment project",
        "private": False,
        "auto_init": True,  # adds a README.md automatically
    }

    # Authentication header
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    # Send the request
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        repo_url = response.json()["html_url"]
        return {"message": "Repository created successfully", "repo_url": repo_url}
    elif response.status_code == 422:
        # Repo already exists
        repo_url = f"https://github.com/{GITHUB_USERNAME}/{repo_name}"
        return {"message": "Repository already exists", "repo_url": repo_url}
    else:
        return {
            "error": "Failed to create repository",
            "status_code": response.status_code,
            "details": response.text,
        }
