from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def root():
    return {"message": "LLM Code Deployment API is running 🚀"}

@app.post("/api-endpoint")
async def api_endpoint(request: Request):
    data = await request.json()
    return {"status": "ok", "received": data}

# Vercel Lambda handler
def handler(event, context):
    from mangum import Mangum
    asgi_handler = Mangum(app)
    return asgi_handler(event, context)
