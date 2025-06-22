import requests
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Evenement
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAGENDA_API_KEY")
AGENDA_SLUG = "biblis-en-folie-2025"

def fetch_openagenda_events():
    url = f"https://api.openagenda.com/v2/agendas/{AGENDA_SLUG}/events"
    params = {
        "key": API_KEY,
        "limit": 50,
        "timezone": "Europe/Paris"
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data.get("events", [])

def save_events(events):
    db: Session = SessionLocal()
    count = 0

    for event in events:
        fields = event.get("description", {})
        titre = event.get("title", {}).get("fr")
        description = fields.get("fr", "")
        location = event.get("location")
        if location and "name" in location and "fr" in location["name"]:
                lieu = location["name"]["fr"]
        else:
                lieu = "inconnu"

        prix = 0.0
        date_str = event.get("timings", [{}])[0].get("start")

        try:
            date = datetime.fromisoformat(date_str)
        except:
            continue

        e = Evenement(
            titre=titre or "Sans titre",
            description=description,
            lieu=lieu,
            prix=prix,
            date=date
        )

        db.add(e)
        count += 1

    db.commit()
    db.close()
    print(f"{count} événements ajoutés à la base.")

if __name__ == "__main__":
    events = fetch_openagenda_events()
    save_events(events)
