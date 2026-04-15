from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.services.claude_service import ClaudeService
from app.models import get_db, init_db, User, Document, Order
from app.auth import hash_password as get_password_hash, authenticate_user, create_access_token, get_current_user
import os
import pathlib
from datetime import datetime, timedelta

app = FastAPI(title="AssistAdmin Pro API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Modèles Pydantic pour les requêtes
class UserRegister(BaseModel):
    username: str
    email: str
    phone: Optional[str] = None
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str

class DocumentCreate(BaseModel):
    document_type: str
    title: str
    content: str
    prompt_used: Optional[str] = None

class OrderCreate(BaseModel):
    document_id: int
    amount: int
    payment_method: str

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
    return {"message": "AssistAdmin Pro API", "status": "online"}

@app.get("/api/status")
async def api_status():
    return {"message": "AssistAdmin Pro API", "status": "online"}

@app.get("/api/test-claude")
async def test_claude():
    cs = ClaudeService()
    result = cs.test_connection()
    return {"test_result": result}

# ========== AUTHENTIFICATION ==========

@app.post("/api/register", response_model=TokenResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Inscription d'un nouvel utilisateur"""
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur ou email déjà utilisé")
    
    # Créer le nouvel utilisateur
    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Créer le token
    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }

@app.post("/api/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Connexion d'un utilisateur existant"""
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }

@app.get("/api/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """Obtenir les informations de l'utilisateur connecté"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "phone": current_user.phone,
        "created_at": current_user.created_at,
        "is_active": current_user.is_active
    }

# ========== DOCUMENTS (protégés) ==========

@app.post("/api/documents")
async def save_document(
    doc_data: DocumentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Sauvegarder un document pour l'utilisateur connecté"""
    document = Document(
        user_id=current_user.id,
        document_type=doc_data.document_type,
        title=doc_data.title,
        content=doc_data.content,
        prompt_used=doc_data.prompt_used
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return {
        "id": document.id,
        "type": document.document_type,
        "title": document.title,
        "created_at": document.created_at
    }

@app.get("/api/documents")
async def get_user_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer tous les documents de l'utilisateur connecté"""
    documents = db.query(Document).filter(Document.user_id == current_user.id).order_by(Document.created_at.desc()).all()
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

@app.get("/api/documents/{document_id}")
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer un document spécifique"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    return {
        "id": document.id,
        "type": document.document_type,
        "title": document.title,
        "content": document.content,
        "prompt_used": document.prompt_used,
        "created_at": document.created_at
    }

# ========== COMMANDES (protégées) ==========

@app.post("/api/orders")
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Créer une commande pour un document"""
    # Vérifier que le document appartient à l'utilisateur
    document = db.query(Document).filter(
        Document.id == order_data.document_id,
        Document.user_id == current_user.id
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    
    order = Order(
        user_id=current_user.id,
        document_id=order_data.document_id,
        amount=order_data.amount,
        payment_method=order_data.payment_method
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return {
        "id": order.id,
        "amount": order.amount,
        "payment_method": order.payment_method,
        "status": order.payment_status
    }

# ========== STATISTIQUES ==========

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Statistiques globales (publique)"""
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
