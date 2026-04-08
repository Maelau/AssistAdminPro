from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.claude_service import ClaudeService

app = FastAPI(title="AssistAdmin Pro API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AssistAdmin Pro API", "status": "online", "claude_ready": False}

@app.get("/test-claude")
async def test_claude():
    cs = ClaudeService()
    result = cs.test_connection()
    return {"test_result": result}
