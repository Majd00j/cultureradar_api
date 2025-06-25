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

@router.get("/", response_model=list[schemas.EvenementResponse])
def read_evenements(limit: int = Query(default=10), offset: int = Query(default=0), db: Session = Depends(get_db)):
    return db.query(models.Evenement).offset(offset).limit(limit).all()

@router.get("/{evenement_id}", response_model=schemas.EvenementResponse)
def read_evenement(evenement_id: int, db: Session = Depends(get_db)):
    evenement = db.query(models.Evenement).filter(models.Evenement.id == evenement_id).first()
    if not evenement:
        raise HTTPException(status_code=404, detail="Événement non trouvé")
    return evenement

@router.get("/search/", response_model=list[schemas.EvenementResponse])
def search_evenements(
    q: str = Query(..., description="Mot-clé dans le titre ou la commune"),
    db: Session = Depends(get_db)
):
    return db.query(models.Evenement).filter(
        (models.Evenement.titre.ilike(f"%{q}%")) |
        (models.Evenement.commune.ilike(f"%{q}%"))
    ).all()
