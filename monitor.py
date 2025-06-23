import os
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

# Load environment variables
TWILIO_SID = os.environ['TWILIO_SID']
TWILIO_AUTH = os.environ['TWILIO_AUTH']
TWILIO_FROM = os.environ['TWILIO_FROM']
TWILIO_TO = os.environ['TWILIO_TO']
LAST_CONTENT_FILE = "last_content.txt"

URL = "https://www.israir.co.il/Passengers_Info/Emergency_Info"
TARGET_CLASS = "component-text__text component-text__text--top"

def fetch_content():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    el = soup.find(class_=TARGET_CLASS)
    return el.get_text(strip=True) if el else ""

def load_last_content():
    if os.path.exists(LAST_CONTENT_FILE):
        with open(LAST_CONTENT_FILE, 'r') as f:
            return f.read()
    return ""

def save_content(text):
    with open(LAST_CONTENT_FILE, 'w') as f:
        f.write(text)

def send_whatsapp(message):
    client = Client(TWILIO_SID, TWILIO_AUTH)
    client.messages.create(
        from_=f'whatsapp:{TWILIO_FROM}',
        to=f'whatsapp:{TWILIO_TO}',
        body=message
    )

def main():
    current = fetch_content()
    last = load_last_content()

    if current != last:
        msg = f"✏️ Update detected on Israir page:\n{current[:500]}"
        send_whatsapp(msg)
        save_content(current)
    else:
        send_whatsapp("No change.")

if __name__ == "__main__":
    main()
