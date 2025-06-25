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
AGENDA_SLUG = "ile-de-france"  # à personnaliser si besoin

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

        if len(page_events) < limit or len(events) >= MAX_EVENTS:
            break

    return events

def save_events(events):
    db: Session = SessionLocal()
    count = 0

    for event in events:
        try:
            titre = event.get("title", {}).get("fr", "Sans titre")
            description = event.get("longDescription", {}).get("fr", "")
            lieu = event.get("location", {}).get("label", {}).get("fr", "inconnu")
            commune = event.get("location", {}).get("city")
            latitude = event.get("location", {}).get("latitude")
            longitude = event.get("location", {}).get("longitude")
            image_url = event.get("image", {}).get("imageFiles", [{}])[0].get("url")
            contact_email = event.get("contact", {}).get("email")
            contact_phone = event.get("contact", {}).get("phone")
            conditions = event.get("conditions")
            age = event.get("audience", {}).get("minAge")

            date_str = event.get("timings", [{}])[0].get("begin")
            if not date_str:
                continue
            date = parse(date_str)

            e = Evenement(
                titre=titre,
                description=description,
                lieu=lieu,
                date=date,
                prix=0.0,
                image_url=image_url,
                commune=commune,
                contact_email=contact_email,
                contact_phone=contact_phone,
                conditions=conditions,
                age=age,
                latitude=latitude,
                longitude=longitude
            )
            db.add(e)
            count += 1
        except Exception as err:
            print(f"Erreur sur un événement : {err}")
            continue

    db.commit()
    db.close()
    print(f"{count} événements ajoutés à la base.")

if __name__ == "__main__":
    events = fetch_openagenda_events()
    print(f"{len(events)} événements récupérés depuis OpenAgenda.")
    save_events(events)
