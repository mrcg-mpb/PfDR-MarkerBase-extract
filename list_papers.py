"""
List the PDF filenames in the shared Drive folder and write them to a file.

The first automated step: a lightweight "what's in the folder right now" index.
It writes ONLY filenames — never any text from inside the papers — so the output
is safe to commit to a public repo.

  Folder ID : from --folder, or the DRIVE_FOLDER_ID env var.
  Key path  : from GOOGLE_APPLICATION_CREDENTIALS.

Run locally:
    export GOOGLE_APPLICATION_CREDENTIALS=~/.secrets/pfdr-markerbase-key.json
    python list_papers.py --folder <FOLDER_ID>

On GitHub Actions both come from repo secrets (see .github/workflows/list-papers.yml).
"""
import argparse
import os
import pathlib
import sys

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
except ImportError:
    sys.exit("Missing deps. Run: pip install google-api-python-client google-auth")

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
OUTPUT = pathlib.Path(__file__).parent / "paper_list.txt"


def drive_service():
    key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not key_path:
        sys.exit("Set GOOGLE_APPLICATION_CREDENTIALS to the service-account key path.")
    creds = service_account.Credentials.from_service_account_file(key_path, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def list_pdf_names(service, folder_id):
    names, page_token = [], None
    while True:  # paginate, in case the folder grows beyond one page
        resp = service.files().list(
            q=f"'{folder_id}' in parents and mimeType='application/pdf' and trashed=false",
            fields="nextPageToken, files(name)",
            pageSize=200,
            pageToken=page_token,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()
        names.extend(f["name"] for f in resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return sorted(names)


def main():
    parser = argparse.ArgumentParser(description="List PDF names in the Drive folder.")
    parser.add_argument("--folder", default=os.environ.get("DRIVE_FOLDER_ID"),
                        help="Drive folder ID (or set DRIVE_FOLDER_ID)")
    args = parser.parse_args()
    if not args.folder:
        sys.exit("Provide --folder or set DRIVE_FOLDER_ID.")

    service = drive_service()
    names = list_pdf_names(service, args.folder)

    OUTPUT.write_text("\n".join(names) + ("\n" if names else ""))
    print(f"Wrote {len(names)} filename(s) to {OUTPUT.name}")
    for n in names:
        print(f"  {n}")


if __name__ == "__main__":
    main()
