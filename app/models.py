from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from app.database import Base

# Table des événements 
class Evenement(Base):
    __tablename__ = "evenements"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, nullable=False)
    description = Column(String)
    lieu = Column(String)
    date = Column(DateTime)
    prix = Column(Float)

# table des utilisateurs
class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    mot_de_passe = Column(String, nullable=False)
   # Préférences culturelles
    musique = Column(Boolean, default=False)
    theatre = Column(Boolean, default=False)
    cinema = Column(Boolean, default=False)
    expositions = Column(Boolean, default=False)