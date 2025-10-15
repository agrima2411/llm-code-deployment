# main.py
import os
import base64
import requests
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

# FastAPI app
app = FastAPI(title="LLM Code Deployment API 🚀")

# GitHub credentials
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
SECRET = os.getenv("SECRET")


# ---------- MODELS ----------

class RepoRequest(BaseModel):
    repo_name: str
    description: str = "Automated repo created via FastAPI"
    private: bool = False


class PushRequest(BaseModel):
    repo_name: str
    filename: str
    content: str
    message: str


class RoundRequest(BaseModel):
    email: str
    secret: str
    task: str
    round: int
    nonce: str
    brief: str
    evaluation_url: str


# ---------- ROUTES ----------

@app.get("/")
def home():
    return {"message": "LLM Code Deployment API is running 🚀"}


# GitHub: Create repo
@app.post("/github/repo")
def create_github_repo(req: RepoRequest):
    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {
        "name": req.repo_name,
        "description": req.description,
        "private": req.private,
        "auto_init": True
    }
    res = requests.post(url, json=data, headers=headers)
    if res.status_code not in (200, 201):
        raise HTTPException(status_code=res.status_code, detail=res.json())
    return {"status": "success", "repo": res.json()}


# GitHub: Push or update file
@app.post("/github/push")
def push_to_repo(req: PushRequest):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{req.repo_name}/contents/{req.filename}"
    encoded_content = base64.b64encode(req.content.encode()).decode()
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    get_res = requests.get(url, headers=headers)
    data = {"message": req.message, "content": encoded_content}
    if get_res.status_code == 200:
        data["sha"] = get_res.json()["sha"]
    res = requests.put(url, json=data, headers=headers)
    if res.status_code not in (200, 201):
        raise HTTPException(status_code=res.status_code, detail=res.json())
    return {"status": "success", "response": res.json()}


# API endpoint for round requests
@app.post("/api-endpoint")
async def handle_round(req: RoundRequest):
    if req.secret != SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")
    
    # Simulate building & deploying an app repo
    repo_name = f"{req.task}-round{req.round}"
    
    # Create repo
    create_github_repo(RepoRequest(repo_name=repo_name, private=False))
    
    # Push README.md
    push_to_repo(PushRequest(
        repo_name=repo_name,
        filename="README.md",
        content=f"# {req.task}\n\nRound {req.round} task\n\n{req.brief}",
        message="Initial commit via API"
    ))
    
    # Normally, would deploy GitHub Pages here
    
    # Respond to evaluation URL
    payload = {
        "email": req.email,
        "task": req.task,
        "round": req.round,
        "nonce": req.nonce,
        "repo_url": f"https://github.com/{GITHUB_USERNAME}/{repo_name}",
        "commit_sha": "mockedsha1234",
        "pages_url": f"https://{GITHUB_USERNAME}.github.io/{repo_name}"
    }
    
    try:
        requests.post(req.evaluation_url, json=payload, headers={"Content-Type": "application/json"})
    except Exception as e:
        print(f"Evaluation callback failed: {e}")
    
    return {"status": "ok", "evaluation_callback_status": "mocked", "repo_url": payload["repo_url"], "commit_sha": payload["commit_sha"], "pages_url": payload["pages_url"]}
