from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
import hashlib

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_mot_de_passe(mdp: str) -> str:
    return hashlib.sha256(mdp.encode()).hexdigest()

@router.post("/", response_model=schemas.UtilisateurResponse)
def create_utilisateur(utilisateur: schemas.UtilisateurCreate, db: Session = Depends(get_db)):
    db_utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.email == utilisateur.email).first()
    if db_utilisateur:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    utilisateur_dict = utilisateur.dict()
    utilisateur_dict["mot_de_passe"] = hash_mot_de_passe(utilisateur_dict["mot_de_passe"])

    new_user = models.Utilisateur(**utilisateur_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=list[schemas.UtilisateurResponse])
def get_utilisateurs(db: Session = Depends(get_db)):
    return db.query(models.Utilisateur).all()

@router.patch("/{id}", response_model=schemas.UtilisateurResponse)
def update_utilisateur(id: int, updates: schemas.UtilisateurUpdate, db: Session = Depends(get_db)):
    utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.id == id).first()

    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    update_data = updates.dict(exclude_unset=True)  # Ne met à jour que les champs fournis

    for key, value in update_data.items():
        setattr(utilisateur, key, value)

    db.commit()
    db.refresh(utilisateur)
    return utilisateur
