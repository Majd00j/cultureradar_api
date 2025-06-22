from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EvenementBase(BaseModel):
    titre: str
    description: str
    lieu: str
    date: datetime
    prix: float

class EvenementCreate(EvenementBase):
    pass

class EvenementResponse(EvenementBase):
    id: int

    class Config:
        orm_mode = True


class UtilisateurBase(BaseModel):
    nom: str
    email: str
    musique: Optional[bool] = False
    theatre: Optional[bool] = False
    cinema: Optional[bool] = False
    expositions: Optional[bool] = False

class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: str  # En clair pour le moment

class UtilisateurResponse(UtilisateurBase):
    id: int

    class Config:
        orm_mode = True

class UtilisateurUpdate(BaseModel):
    nom: Optional[str] = None
    email: Optional[str] = None
    musique: Optional[bool] = None
    theatre: Optional[bool] = None
    cinema: Optional[bool] = None
    expositions: Optional[bool] = None