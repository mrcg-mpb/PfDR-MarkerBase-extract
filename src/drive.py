"""
Google Drive access for the MarkerBase pipeline.

Read-only (drive.readonly). Credentials come from GOOGLE_APPLICATION_CREDENTIALS
(a path to the service-account JSON key). See NOTES.md.

The inbox is a tree: a top folder (e.g. `papers`) holds a `master` subfolder of
your own PDFs plus one subfolder per contributor. Each contributor is shared only
their own subfolder, so they can't see the others; the service account is shared
the top folder, so it sees everything. We therefore WALK the tree (read-only,
never moving anything) and collect every PDF, tagging each with the folder it
came from. Supplements use the same shape: a `<paper-id>` folder may live under
any contributor's subfolder, so we search for it by name anywhere in the tree.
"""
import hashlib
import io
import os
import sys

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
except ImportError:
    sys.exit("Missing Google deps. Run: pip install google-api-python-client google-auth")

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
FOLDER_MIME = "application/vnd.google-apps.folder"
MAX_DEPTH = 5  # guard against pathological nesting / cycles


def service():
    key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not key_path:
        sys.exit("Set GOOGLE_APPLICATION_CREDENTIALS to the service-account key path.")
    creds = service_account.Credentials.from_service_account_file(key_path, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def _list_folder(svc, folder_id):
    """List the direct children of a folder (files and subfolders)."""
    out, token = [], None
    while True:
        resp = svc.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken, files(id, name, mimeType, md5Checksum, size, modifiedTime)",
            pageSize=200,
            pageToken=token,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()
        out.extend(resp.get("files", []))
        token = resp.get("nextPageToken")
        if not token:
            break
    return out


def _is_pdf(f):
    return f.get("mimeType") == "application/pdf" or f["name"].lower().endswith(".pdf")


def list_pdfs(svc, root_id):
    """Walk the tree under root_id; return [{'name','id','source'}, ...].

    `source` is the name of the folder a PDF sits in ('' for the root itself) —
    i.e. which contributor (or `master`) it came from.
    """
    out = []

    def walk(folder_id, source, depth):
        for f in _list_folder(svc, folder_id):
            if f["mimeType"] == FOLDER_MIME:
                if depth < MAX_DEPTH:
                    walk(f["id"], f["name"], depth + 1)
            elif _is_pdf(f):
                out.append({"name": f["name"], "id": f["id"], "source": source})

    walk(root_id, "", 0)
    return out


def find_named_folders(svc, root_id, name):
    """Return every folder named `name` anywhere under root_id (any contributor)."""
    found, frontier = [], [(root_id, 0)]
    while frontier:
        fid, depth = frontier.pop()
        for f in _list_folder(svc, fid):
            if f["mimeType"] != FOLDER_MIME:
                continue
            if f["name"] == name:
                found.append(f)
            if depth < MAX_DEPTH:
                frontier.append((f["id"], depth + 1))
    return found


def fetch_bytes(svc, file_id):
    """Download a file's bytes straight into memory (never touches disk)."""
    request = svc.files().get_media(fileId=file_id, supportsAllDrives=True)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return buf.getvalue()


def _supplement_files(svc, supplement_root_id, stem):
    """Every non-folder file across all `<stem>` supplement folders."""
    for folder in find_named_folders(svc, supplement_root_id, stem):
        for f in _list_folder(svc, folder["id"]):
            if f["mimeType"] != FOLDER_MIME:
                yield f


def fetch_supplement_files(svc, supplement_root_id, stem):
    """Return [{'name', 'bytes'}, ...] for every file in any `<stem>` supplement
    folder — ALL types, not just PDFs. The supplements loader decides what it can
    convert; unreadable formats are skipped there, not here."""
    return [{"name": f["name"], "bytes": fetch_bytes(svc, f["id"])}
            for f in _supplement_files(svc, supplement_root_id, stem)]


def supplement_fingerprint(svc, supplement_root_id, stem):
    """A stable digest of the `<stem>` folder's contents, so the eligibility
    re-check can tell when new/changed files have been uploaded (rather than
    re-billing on an unchanged folder). Empty string if no folder/files."""
    items = sorted(
        (f["name"], f.get("md5Checksum") or f.get("modifiedTime") or f.get("size") or "")
        for f in _supplement_files(svc, supplement_root_id, stem))
    if not items:
        return ""
    return hashlib.sha1(repr(items).encode("utf-8")).hexdigest()[:16]
