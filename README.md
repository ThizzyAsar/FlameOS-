# TM3-FlameVault

## Setup
1. Clone this repo to ~/TM3-FlameVault
2. Copy `.env` into `~/.env` and lock permissions: `chmod 600 ~/.env`
3. Create & activate venv:
   ```bash
   python3 -m venv ~/flame-env
   source ~/flame-env/bin/activate
   pip install -r requirements.txt
   ```
4. Enable auto-uploader service (loads env vars from `~/.env`):
   ```bash
   sudo cp flame-uploader.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable flame-uploader
   sudo systemctl start flame-uploader
   ```
5. Set up daily PDF generator via cron:
   ```bash
   crontab -e
   # Add:
   0 0 * * * source ~/flame-env/bin/activate && python ~/TM3-FlameVault/generate_scroll_pdf.py
   # Optionally specify output directory with --out
   ```

The scripts will exit with a clear message if required environment
variables (`PINATA_JWT` or `FLAMEVAULT_PATH`) are missing.

## Usage
- Drop .docx/.pdf into $FLAMEVAULT_PATH/scrolls → auto-upload & index
- Run manual index: `flame-search index $FLAMEVAULT_PATH/scrolls/*`
- Query: `flame-search --query "your term"`
