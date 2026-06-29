# MarkerBase pipeline — notes

## How the Google Drive access works

There are **two separate worlds**, linked by one deliberate act:

- **Google Cloud** — where *automation* lives (the robot identity + its credentials).
- **Google Drive** — where the *data* (PDFs) lives.

The Cloud project does **not** contain your Drive. They are connected **only** by
**sharing a folder** with the robot's email. Without that share, the robot is a
valid identity that can see none of your files.

### The elements

| Element | What it is | Analogy |
|---|---|---|
| Google account (`<project-account>@gmail.com`) | A *human* login that owns things | You, the person |
| Cloud project (`<your-project>`) | Container for APIs + identities you create | A company you registered |
| Drive API (enabled) | Switch allowing the project to talk to Drive | Permission to do Drive work at all |
| Service account (`markerbase-reader`) | A *non-human* robot identity scripts log in as | A robot employee you hired |
| Service-account email | The robot's address; how Drive grants it access | The name on the room's access list |
| JSON key file | The robot's credential ("this script IS that robot") | The employee's keycard |
| Scope (`drive.readonly`) | What the robot may do — read only | A read-only badge |
| Drive folder (`inbox_test`) | A normal folder holding the PDFs | A room you own |
| The share (folder → robot, Viewer) | Adds the robot to that folder's access list | Putting the robot on the entry list |

### How they nest

```
YOUR GOOGLE ACCOUNT  (a human login)
│
├── GOOGLE CLOUD
│     └── Project: <your-project>
│           ├── Drive API: ENABLED
│           └── Service account: markerbase-reader
│                 ├── email:  markerbase-reader@<your-project>.iam.gserviceaccount.com  ← its "name"
│                 └── JSON key (downloaded)          ← its "password"
│
└── GOOGLE DRIVE
      └── Folder: <inbox folder>
            ├── example.pdf
            └── Shared with → markerbase-reader@…  (Viewer)   ← THE LINK
```

(The project and the Drive can even live on different Google accounts — they're
only ever linked by the share. The real project ID, service-account email, and
folder ID are kept out of this public repo — they live in your local env vars
and GitHub secrets.)

### The key idea: identity vs. access

Two separate questions, both must be true:

- **Authentication — "who is making this request?"** → answered by the **JSON key**.
- **Authorization — "is that identity allowed to see this folder?"** → answered by the **share**.

The key proves *who*; the share grants *what*. Neither alone is enough.

### Runtime flow (what a Drive script does)

1. Read `GOOGLE_APPLICATION_CREDENTIALS` → find the JSON key.
2. Use the key to prove "I am `markerbase-reader`" → get a short-lived token. *(auth)*
3. Ask the Drive API to list/read files in folder X.
4. Drive checks the share: is `markerbase-reader` allowed? Yes, Viewer, read-only. *(authz)*
5. Drive returns the file. No browser login, no personal password used.

### Why this structure

- Your personal Google login is never in the code.
- Least privilege: the robot can only *read*, only the folders you *shared*.
- Small blast radius: a leaked key = read access to one folder; delete/rotate the
  key in the Cloud console without touching your account.

## The two credentials in the pipeline

The full pipeline talks to two external services, each with its own credential:

| Credential | Env var | Used for | Billed to |
|---|---|---|---|
| Google service-account key | `GOOGLE_APPLICATION_CREDENTIALS` | *Fetching* papers from Drive | Free (Drive API) |
| Anthropic API key | `ANTHROPIC_API_KEY` | *Assessing* papers | API credit |

A terminal running the whole flow needs **both** set. They're independent
accounts, credentials, and bills.

## Secret hygiene

- Both secrets live **outside** the repo (`~/.secrets/…`), referenced via env vars.
- `.gitignore` is a backstop (excludes key files, `.env`, `papers/`).
- The real protection is keeping the JSON key out of the project folder entirely.
