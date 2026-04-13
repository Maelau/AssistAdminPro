from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.services.claude_service import ClaudeService
import os

app = FastAPI(title="AssistAdmin Pro API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir l'interface web (fichier HTML)
@app.get("/")
async def root():
    # Vérifier si le fichier index.html existe, sinon retourner le JSON d'API
    index_path = "templates/index.html"
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "AssistAdmin Pro API", "status": "online", "claude_ready": False}

@app.get("/api/status")
async def api_status():
    return {"message": "AssistAdmin Pro API", "status": "online", "claude_ready": False}

@app.get("/api/test-claude")
async def test_claude():
    cs = ClaudeService()
    result = cs.test_connection()
    return {"test_result": result}
