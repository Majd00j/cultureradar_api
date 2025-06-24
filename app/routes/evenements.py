from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas

router = APIRouter(prefix="/evenements", tags=["Evenements"])

# Permet d'ouvrir une session DB pour chaque requête
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.EvenementResponse)
def create_evenement(evenement: schemas.EvenementCreate, db: Session = Depends(get_db)):
    db_event = models.Evenement(**evenement.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/evenements/", response_model=list[models.EvenementOut])  # <-- Ajoute les paramètres ici
def read_evenements(limit: int = Query(default=10), offset: int = Query(default=0), db: Session = Depends(get_db)):
    return db.query(models.Evenement).offset(offset).limit(limit).all()