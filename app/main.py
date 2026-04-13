from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.services.claude_service import ClaudeService
from app.models import get_db, init_db, User, Document, Order
import os
import pathlib
from datetime import datetime

app = FastAPI(title="AssistAdmin Pro API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiser la base de données au démarrage
@app.on_event("startup")
def startup_event():
    init_db()

# Obtenir le chemin absolu du répertoire courant
BASE_DIR = pathlib.Path(__file__).parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
INDEX_HTML = TEMPLATES_DIR / "index.html"

@app.get("/")
async def root():
    if INDEX_HTML.exists():
        return FileResponse(INDEX_HTML)
    return {"message": "AssistAdmin Pro API", "status": "online", "claude_ready": False}

@app.get("/api/status")
async def api_status():
    return {"message": "AssistAdmin Pro API", "status": "online", "claude_ready": False}

@app.get("/api/test-claude")
async def test_claude():
    cs = ClaudeService()
    result = cs.test_connection()
    return {"test_result": result}

# Endpoints pour la gestion des utilisateurs
@app.post("/api/users")
async def create_user(username: str, email: str, phone: str = None, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")
    
    user = User(username=username, email=email, phone=phone)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username, "email": user.email, "phone": user.phone}

# Endpoints pour les documents
@app.post("/api/documents")
async def save_document(user_id: int, document_type: str, title: str, content: str, prompt_used: str = None, db: Session = Depends(get_db)):
    document = Document(
        user_id=user_id,
        document_type=document_type,
        title=title,
        content=content,
        prompt_used=prompt_used
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return {"id": document.id, "type": document.document_type, "title": document.title, "created_at": document.created_at}

@app.get("/api/documents/{user_id}")
async def get_user_documents(user_id: int, db: Session = Depends(get_db)):
    documents = db.query(Document).filter(Document.user_id == user_id).order_by(Document.created_at.desc()).all()
    return [
        {
            "id": doc.id,
            "type": doc.document_type,
            "title": doc.title,
            "status": doc.status,
            "created_at": doc.created_at
        }
        for doc in documents
    ]

# Endpoint pour les commandes
@app.post("/api/orders")
async def create_order(user_id: int, document_id: int, amount: int, payment_method: str, db: Session = Depends(get_db)):
    order = Order(
        user_id=user_id,
        document_id=document_id,
        amount=amount,
        payment_method=payment_method
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return {"id": order.id, "amount": order.amount, "status": order.payment_status}

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    users_count = db.query(User).count()
    documents_count = db.query(Document).count()
    orders_count = db.query(Order).count()
    total_revenue = db.query(Order).filter(Order.payment_status == "completed").with_entities(Order.amount).all()
    total = sum(r[0] for r in total_revenue) if total_revenue else 0
    
    return {
        "users": users_count,
        "documents": documents_count,
        "orders": orders_count,
        "revenue_fcfa": total
    }
