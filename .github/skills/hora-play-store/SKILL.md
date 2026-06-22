---
name: hora-play-store
description: Publish and manage a "Hora"-family Android app on Google Play — store listing, the App Signing SHA that makes Google Sign-In work for testers, the store icon, and track promotion. Use for Play Console / closed-testing tasks, "testers can't sign in", or store-icon work.
---

# Hora Play Store (signing SHA, store icon, listing, tracks)

## "No Google account exists" for testers = the Play App Signing SHA is missing
Google Play **re-signs** every Play-distributed build with its own *App Signing key* — a
different SHA than your upload/debug keys. Google Sign-In authorises the caller by
(package + signing SHA), so a build that signs in fine when sideloaded **fails for every Play
tester**. Via Credential Manager it surfaces as `NoCredentialException` ("No Google accounts
found") even though accounts exist — NOT a `DEVELOPER_ERROR` (the code is fine if it already uses
`setFilterByAuthorizedAccounts(false)`).

**Fix — server-side, no rebuild, no re-review:**
1. Play Console → **App integrity** (use the search box: type `app signing`; it's not under the
   Testing list) → **App signing key certificate** (the upper one, not "Upload key certificate").
2. Copy its SHA-1 and SHA-256.
3. Get the Firebase app id: `firebase apps:list ANDROID --project <proj>`.
4. Add both (SHA-256 is required for Credential Manager):
   `firebase apps:android:sha:create <appId> <SHA> --project <proj>`.
5. Verify: `firebase apps:android:sha:list <appId> --project <proj>`. Testers retry in ~5–15 min.

## The store icon ≠ the launcher icon
The adaptive launcher foreground keeps safe-zone padding (the glyph fills only a small bounding
circle) — fine on-device (the launcher masks/zooms) but it looks tiny in the Play listing, which
renders the store icon almost as-is. Match each app's own **live store icon** metrics rather than
assuming a fixed family constant:
- `curl` the live icon via the listing's `og:image` (`play.google.com/store/apps/details?id=<pkg>`
  at `=s512`).
- Measure the ink bounding box on that reference → height fraction, vertical/horizontal center.
- Render the new icon at the same metrics on the same canvas size/background. Launcher mipmaps
  stay untouched — this is a separate asset.

## Setting the store icon — use the edits.images API (don't fight the browser)
The 512 store icon can be set **non-interactively** with the AndroidPublisher **edits** API, with the
same publisher service account that uploads bundles — even when the full listing bootstrap /
`publishListing` is blocked (see below). `icon` is a single-image type, so upload replaces:
```python
svc = build("androidpublisher","v3",credentials=sa_creds)          # scope .../androidpublisher
eid = svc.edits().insert(packageName=PKG, body={}).execute()["id"]
svc.edits().images().upload(packageName=PKG, editId=eid, language="<listing locale, e.g. en-GB>",
    imageType="icon", media_body=MediaFileUpload(icon_512_png, mimetype="image/png")).execute()
svc.edits().validate(packageName=PKG, editId=eid).execute()         # catch issues before publishing
svc.edits().commit(packageName=PKG, editId=eid).execute()           # commit = live
```
Verify by re-listing on a fresh edit (`edits().images().list(... imageType="icon")`) and diffing the
served `url` bytes against the source. Use the app's actual listing locale (`edits().listings().list`).

**Why not the console UI:** agent automation of **Add assets -> Upload** is unreliable — the in-page
picker fires a **native OS file dialog** (not drivable from the browser tools), and the browser
file-upload tool only accepts files the harness registered, so it **rejects repo paths**. A human
clicking Upload works fine; for automation, prefer the API above.

## Tracks & promotion
- `internal` publishes immediately via API.
- internal → closed (alpha): `promoteReleaseArtifact --from-track internal --promote-track alpha
  --release-status completed` (use `draft` only while the app itself is still a draft, then roll
  out in console). alpha (closed) → beta (open) → production likewise.
- **Gate before production:** Play requires roughly 12 testers × 14 continuous days on a closed
  test before a new app/account can reach production — a one-time unlock, not a per-release gate.
  Updating the closed version does not reset the clock.
- **Version-code precedence:** when a user is eligible for builds on multiple tracks, Play serves
  the **highest version code**, not the highest-priority track. You can't have the same build
  artifact on two tracks simultaneously — to put a build on Open Testing while another sits in
  Production, bump the version code first. ("Production is King" holds only because it usually
  carries the highest code.)
- **Launch-day exception:** for an external/marketing launch, target Production with a direct
  link — a "Join Beta → wait → install" flow adds friction that hurts launch-day conversion.

## Listing API is often blocked on fresh apps — enter listing manually
`publishReleaseListing` / bootstrap calls can 404 ("listing not found" / "migrate to new
publishing API") because the service account lacks full store-listing permission (the `edits().images()` icon /
graphics upload above still works — see "Setting the store icon"). Enter the rest of the store
listing by hand in console: copy, feature graphic (1024×500), phone screenshots
(≤ 2:1, e.g. 1080×2160), and the content rating / data safety / target audience / ads
declarations.

## Security
The Play Console service-account key is gitignored — never commit/print it. See
`hora-app-release` for the full no-secrets checklist.
