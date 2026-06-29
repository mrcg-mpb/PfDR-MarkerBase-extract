"""
Experiment 8 — Drive → eligibility in one step.

Pulls a PDF straight from the shared Drive folder (in memory — no local copy)
and assesses it for eligibility. This is the shape the eventual watcher will
use: a file appears in Drive, the pipeline reads it and judges it.

It combines:
  - the Drive service-account access from script 07
  - the eligibility assessment, now living in markerbase.py

Setup (once):
    pip install google-api-python-client google-auth anthropic pydantic

Each terminal session — BOTH credentials are needed (Drive to fetch, Anthropic to assess):
    export GOOGLE_APPLICATION_CREDENTIALS=~/.secrets/pfdr-markerbase-key.json
    export ANTHROPIC_API_KEY=sk-ant-...

Run (pick the paper by name or by Drive file ID):
    python 08_assess_from_drive.py --folder <FOLDER_ID> --name 8888283.pdf
    python 08_assess_from_drive.py --folder <FOLDER_ID> --id 1fmZJ... --model opus
"""
import argparse
import io
import os
import sys

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
except ImportError:
    sys.exit("Missing Google deps. Run:\n  pip install google-api-python-client google-auth")

import markerbase  # the shared schema + assessment core

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def drive_service():
    key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not key_path:
        sys.exit("Set GOOGLE_APPLICATION_CREDENTIALS to your service-account JSON key path.")
    creds = service_account.Credentials.from_service_account_file(key_path, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def find_id_by_name(service, folder_id, name):
    resp = service.files().list(
        q=f"'{folder_id}' in parents and name = '{name}' and trashed=false",
        fields="files(id, name)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
    ).execute()
    files = resp.get("files", [])
    if not files:
        sys.exit(f"'{name}' not found in that folder (check the exact filename).")
    return files[0]["id"]


def fetch_bytes(service, file_id):
    request = service.files().get_media(fileId=file_id, supportsAllDrives=True)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return buf.getvalue()


def main():
    parser = argparse.ArgumentParser(description="Fetch a paper from Drive and assess eligibility.")
    parser.add_argument("--folder", required=True, help="Drive folder ID")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--name", help="PDF filename within the folder")
    group.add_argument("--id", dest="file_id", help="Drive file ID (unambiguous)")
    parser.add_argument("--model", choices=markerbase.MODELS, default="haiku",
                        help="which model to use (default: haiku)")
    args = parser.parse_args()

    service = drive_service()

    # Resolve the file, then pull its bytes straight into memory.
    file_id = args.file_id or find_id_by_name(service, args.folder, args.name)
    label = args.name or args.file_id
    print(f"Fetching {label} from Drive …")
    pdf_bytes = fetch_bytes(service, file_id)
    print(f"Got {len(pdf_bytes)} bytes. Assessing with {args.model} …")

    # Hand the bytes straight to the shared assessor — never touches disk.
    resp = markerbase.assess_pdf_bytes(pdf_bytes, model_key=args.model)
    markerbase.report(resp, args.model)


if __name__ == "__main__":
    main()
