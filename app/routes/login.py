from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.auth import create_access_token
import hashlib

router = APIRouter(tags=["Login"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_mot_de_passe(mdp: str) -> str:
    return hashlib.sha256(mdp.encode()).hexdigest()

@router.post("/login")
def login(email: str, mot_de_passe: str, db: Session = Depends(get_db)):
    user = db.query(models.Utilisateur).filter(models.Utilisateur.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    if user.mot_de_passe != hash_mot_de_passe(mot_de_passe):
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")

    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer", "user_id": user.id}
