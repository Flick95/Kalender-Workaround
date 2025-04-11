import requests
from icalendar import Calendar, Event
from datetime import timedelta
from pathlib import Path

# Original iCal-Link
ICAL_URL = "https://modulverwaltung.rlp.de/sembbs/dispatch.php/ical/index/TTJB6wS5"

# Ziel-Datei
OUTPUT_FILE = Path("docs/rlp_kalender_cleaned.ics")

def fetch_and_clean_calendar():
    response = requests.get(ICAL_URL)
    response.raise_for_status()

    original_cal = Calendar.from_ical(response.content)
    new_cal = Calendar()
    new_cal.add('prodid', '-//Bereinigter RLP Kalender//')
    new_cal.add('version', '2.0')

    for component in original_cal.walk():
        if component.name == "VEVENT":
            new_event = Event()
            new_event.add('summary', component.get('summary'))
            new_event.add('dtstart', component.get('dtstart').dt)
            new_event.add('dtend', component.get('dtend').dt)
            new_event.add('location', component.get('location'))
            new_event.add('description', component.get('description'))

            # Beispiel-Regel: Wöchentliche Wiederholung, wenn identische Titel mehrfach auftauchen
            new_event.add('rrule', {'freq': 'weekly', 'count': 10})

            new_cal.add_component(new_event)

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "wb") as f:
        f.write(new_cal.to_ical())

if __name__ == "__main__":
    fetch_and_clean_calendar()
