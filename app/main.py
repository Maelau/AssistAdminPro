from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.services.claude_service import ClaudeService
import os
import pathlib

app = FastAPI(title="AssistAdmin Pro API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Obtenir le chemin absolu du répertoire courant
BASE_DIR = pathlib.Path(__file__).parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
INDEX_HTML = TEMPLATES_DIR / "index.html"

@app.get("/")
async def root():
    # Vérifier si le fichier index.html existe
    if INDEX_HTML.exists():
        return FileResponse(INDEX_HTML)
    # Fallback: retourner le statut API
    return {"message": "AssistAdmin Pro API", "status": "online", "claude_ready": False}

@app.get("/api/status")
async def api_status():
    return {"message": "AssistAdmin Pro API", "status": "online", "claude_ready": False}

@app.get("/api/test-claude")
async def test_claude():
    cs = ClaudeService()
    result = cs.test_connection()
    return {"test_result": result}
