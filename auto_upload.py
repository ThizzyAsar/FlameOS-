import os, requests
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

load_dotenv()
JWT = os.getenv("PINATA_JWT")
WATCH_DIR = os.getenv("FLAMEVAULT_PATH")

class FlameHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.lower().endswith(('.pdf','.docx')):
            self.upload(event.src_path)

    def upload(self, filepath):
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        headers = {"Authorization": f"Bearer {JWT}"}
        with open(filepath,'rb') as f:
            resp = requests.post(url, headers=headers, files={'file': f})
        data = resp.json()
        print(f"📡 Uploaded: {filepath} — CID: {data.get('IpfsHash')}")

if __name__ == "__main__":
    os.makedirs(WATCH_DIR, exist_ok=True)
    handler = FlameHandler()
    obs = Observer()
    obs.schedule(handler, WATCH_DIR, recursive=False)
    obs.start()
    try:
        obs.join()
    except KeyboardInterrupt:
        obs.stop()
