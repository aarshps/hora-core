---
name: hora-bitwarden-secrets
description: Retrieve and manage Hora-family Android build secrets (signing keystore, Firebase config, Play Console service-account key) from Bitwarden. Use when a build fails due to a missing keystore/google-services.json, when starting in a fresh environment, or when saving/rotating a secret.
---

# Hora Bitwarden secrets workflow

Production signing keys and Firebase configs are never committed. They live in Bitwarden, one
secure note per app (commonly grouped under a shared folder/collection — confirm the exact
folder/item name per app, don't assume one is universal).

## Master password location
Each app's `android/.env.local` (gitignored):
```
BW_PASSWORD='<master password>'
```

## Non-interactive unlock (Windows Bash)
```bash
BW_SESSION=$(bw unlock "$(grep -oP "(?<=BW_PASSWORD=').*(?=')" android/.env.local)" --raw)
bw --session "$BW_SESSION" status   # verify unlocked
```
On Windows, `bw` resolves to `%APPDATA%\npm\bw.cmd`. When calling from a Python `subprocess`, use
the full `.cmd` path explicitly — PATH resolution for `.cmd` shims from a subprocess is unreliable.

## What to recover (per app — exact field names vary; confirm against the app's own secure note)
| Item | Typically stored as |
| --- | --- |
| `app/google-services.json` | secure note → base64 field |
| Upload keystore (`*-upload-key`) | secure note → attachment, base64 |
| Keystore passwords | secure note → `RELEASE_STORE_PASSWORD`, `RELEASE_KEY_ALIAS`, `RELEASE_KEY_PASSWORD` |
| Play Console service-account key | secure note → base64 field |
| Store-reviewer test account | a Bitwarden login item |

## Creating/updating a vault item
Direct heredoc injection into `bw create item` fails on Windows — use `bw encode`:
```bash
ENCODED=$(python3 -c "
import json, subprocess
item = {'object': 'item', 'type': 2, 'name': 'My Item', 'notes': '...'}
enc = subprocess.run(['bw', 'encode'], input=json.dumps(item), capture_output=True, text=True)
print(enc.stdout.strip())
")
bw --session "$BW_SESSION" create item "$ENCODED"
```
For login items (`type: 1`), include a `login` object with `username`, `password`, `uris`.

## When to run this
- Build fails with a missing `google-services.json` or keystore.
- Starting in a fresh environment/machine.
- Saving or rotating a secret (`bw create item` / `bw edit item`).

## Security
Never print a decoded secret value to a transcript or commit it. This skill documents the
*mechanism* only — no real vault item names, folder names, or account emails belong here, since
`hora-core` is public.
