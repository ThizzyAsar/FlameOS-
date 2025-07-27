"""Automatically upload new files to Pinata IPFS."""

import os
import time
import requests
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

load_dotenv()
JWT = os.getenv("PINATA_JWT")
WATCH_DIR = os.getenv("FLAMEVAULT_PATH")

if not JWT or not WATCH_DIR:
    raise EnvironmentError(
        "Required environment variables PINATA_JWT or FLAMEVAULT_PATH are missing."
    )

class FlameHandler(FileSystemEventHandler):
    """Handles new file events by uploading them to IPFS."""

    def on_created(self, event):
        """Upload newly created PDF or DOCX files."""
        if event.src_path.lower().endswith((".pdf", ".docx")):
            self.upload(event.src_path)

    def upload(self, filepath):
        """Send the file to Pinata and report the resulting CID."""
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        headers = {"Authorization": f"Bearer {JWT}"}
        try:
            with open(filepath, "rb") as f:
                resp = requests.post(url, headers=headers, files={"file": f})
            resp.raise_for_status()
            data = resp.json()
            print(f"📡 Uploaded: {filepath} — CID: {data.get('IpfsHash')}")
        except requests.RequestException as exc:
            print(f"⚠️ Failed to upload {filepath}: {exc}")

if __name__ == "__main__":
    """Start the watchdog observer and process events until interrupted."""

    os.makedirs(WATCH_DIR, exist_ok=True)
    handler = FlameHandler()
    obs = Observer()
    obs.schedule(handler, WATCH_DIR, recursive=False)
    obs.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping observer...")
    finally:
        obs.stop()
        obs.join()
