from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import ping

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # temporairement tout autoriser
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ping.router)

from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

from app.routes import ping, evenements  # ajoute "evenements"

app = FastAPI()
# ... (CORS config)
app.include_router(ping.router)
app.include_router(evenements.router)  # ajoute cette ligne

from app.routes import ping, evenements, utilisateurs  # ← ajouter utilisateurs

# ...
app.include_router(ping.router)
app.include_router(evenements.router)
app.include_router(utilisateurs.router)  # ← ajouter cette ligne


from app.routes import ping, evenements, utilisateurs, login

app.include_router(ping.router)
app.include_router(evenements.router)
app.include_router(utilisateurs.router)
app.include_router(login.router)  # ← ajoute cette ligne
