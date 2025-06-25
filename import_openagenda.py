import requests
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Evenement
from datetime import datetime
from dateutil.parser import parse
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAGENDA_API_KEY")
AGENDA_SLUG = "ile-de-france"  # change si tu veux un autre agenda

def fetch_openagenda_events():
    url = f"https://api.openagenda.com/v2/agendas/{AGENDA_SLUG}/events"
    events = []
    limit = 100
    offset = 0
    MAX_EVENTS = 1000 

    while True:
        params = {
            "key": API_KEY,
            "limit": limit,
            "offset": offset,
            "timezone": "Europe/Paris",
            "detailed": 1,
            "startsAfter": "2024-01-01"
        }

        response = requests.get(url, params=params)
        data = response.json()
        page_events = data.get("events", [])

        if not page_events:
            break

        events.extend(page_events)
        offset += limit

        print(f"Page avec {len(page_events)} événements — total récupéré : {len(events)}")

        if len(page_events) < limit or len(events) >= MAX_EVENTS:
            break

    return events

def save_events(events):
    db: Session = SessionLocal()
    count = 0

    for event in events:
        image_url = event.get("image", {}).get("versions", {}).get("large", {}).get("url")
        titre = event.get("title", {}).get("fr", "Sans titre")
        description = event.get("description", {}).get("fr", "")

        location = event.get("location")
        if isinstance(location, dict):
            name = location.get("name")
            if isinstance(name, dict):
                lieu = name.get("fr", "inconnu")
            elif isinstance(name, str):
                lieu = name
            else:
                lieu = "inconnu"
        elif isinstance(location, str):
            lieu = location
        else:
            lieu = "inconnu"

        date_str = event.get("timings", [{}])[0].get("begin")
        if not date_str:
            continue

        try:
            date = parse(date_str)
        except:
            continue

        try:
            e = Evenement(
                titre=titre,
                description=description,
                lieu=lieu,
                date=date,
                prix=0.0,
                image_url=image_url
            )
            db.add(e)
            count += 1
        except:
            continue

    db.commit()
    db.close()
    print(f"{count} événements ajoutés à la base.")

if __name__ == "__main__":
    events = fetch_openagenda_events()
    print(f"{len(events)} événements récupérés depuis OpenAgenda.")
    save_events(events)
