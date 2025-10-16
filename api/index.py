from fastapi import FastAPI, Request
from app.main import verify_secret, parse_request, build_evaluation_payload

app = FastAPI()

@app.get("/")
def root():
    return {"message": "LLM Code Deployment API is running 🚀"}

@app.post("/api-endpoint")
async def api_endpoint(request: Request):
    data = await request.json()
    parsed = parse_request(data)

    # Check secret
    if not verify_secret(parsed.get("secret", "")):
        return {"status": "error", "message": "Invalid secret"}

    payload = build_evaluation_payload(
        parsed,
        repo_url="https://github.com/your-username/repo",
        commit_sha="abc123",
        pages_url="https://your-username.github.io/repo"
    )

    return {"status": "ok", "payload": payload}
