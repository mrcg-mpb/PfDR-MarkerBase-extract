"""
Experiment 7 — Pull a paper from Google Drive (service-account access).

This proves Drive access in isolation, before wiring it into the assessor.
It authenticates as the service account (not as you), lists the PDFs in a
shared folder, and optionally downloads one into ./papers.

The service account reads files because you SHARED the folder with its email —
it has no special powers otherwise. Read-only scope, so it can't modify or
delete anything.

Setup (once):
    pip install google-api-python-client google-auth

Each terminal session — point at your key file (same per-terminal idea as the
Anthropic key, so it never leaks into Claude Code or git):
    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-key.json

Run:
    python 07_drive_pull.py --folder <FOLDER_ID>                 # list PDFs
    python 07_drive_pull.py --folder <FOLDER_ID> --get NAME.pdf  # download into ./papers
"""
import argparse
import io
import os
import pathlib
import sys

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
except ImportError:
    sys.exit("Missing dependencies. Run:\n  pip install google-api-python-client google-auth")

# Read-only is all we need — least privilege.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
PAPERS_DIR = pathlib.Path(__file__).parent / "papers"


def drive_service():
    key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not key_path:
        sys.exit("Set GOOGLE_APPLICATION_CREDENTIALS to your service-account JSON key path,\n"
                 "e.g.  export GOOGLE_APPLICATION_CREDENTIALS=~/.secrets/pfdr-markerbase-key.json")
    creds = service_account.Credentials.from_service_account_file(key_path, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def list_files(service, folder_id):
    resp = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields="files(id, name, mimeType, size, modifiedTime)",
        pageSize=200,
        supportsAllDrives=True,        # harmless for My Drive; needed if you move to a Shared Drive
        includeItemsFromAllDrives=True,
    ).execute()
    return resp.get("files", [])


def download(service, file_id, dest_path):
    request = service.files().get_media(fileId=file_id, supportsAllDrives=True)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    dest_path.write_bytes(buf.getvalue())


def main():
    parser = argparse.ArgumentParser(description="List/download papers from a shared Drive folder.")
    parser.add_argument("--folder", required=True, help="Drive folder ID (from the folder's URL)")
    parser.add_argument("--get", help="filename to download into ./papers")
    args = parser.parse_args()

    service = drive_service()
    files = list_files(service, args.folder)

    if not files:
        print("No files visible to the service account in that folder.\n"
              "Check: (1) the folder ID is correct, and (2) you shared the folder\n"
              "with the service-account email (Viewer).")
        return

    print(f"{len(files)} item(s) the service account can see:")
    for f in files:
        size = f.get("size", "?")
        print(f"  {f['name']}  ({f['mimeType']}, {size} bytes)  id={f['id']}")

    if args.get:
        match = next((f for f in files if f["name"] == args.get), None)
        if not match:
            sys.exit(f"\n'{args.get}' not found in that folder — check the exact filename above.")
        PAPERS_DIR.mkdir(exist_ok=True)
        dest = PAPERS_DIR / match["name"]
        download(service, match["id"], dest)
        print(f"\nDownloaded → {dest}")
        print("You can now assess it:  python 06_assess_paper.py --paper "
              f"{match['name']}")


if __name__ == "__main__":
    main()
