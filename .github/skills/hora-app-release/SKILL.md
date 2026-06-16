---
name: hora-app-release
description: Build and roll out a release of a "Hora"-family Android app (Pathivu, Varisankya, future siblings) — bump version, build the signed release, publish to Google Play, and cut a GitHub release with an installable APK. Use when the user asks to "release / roll out / ship a beta / cut a new build". Enforces the no-secrets rule.
---

# Hora app release (build → Play → GitHub)

Family-wide shape: version bump → signed build → security check → commit/tag/push → GitHub
release → Play upload → track promotion → docs/wiki/memory update. **Per-app values vary —
verify each one against the app's own `app/build.gradle.kts` and its wiki's Build & Release page
before using a number from this skill.**

## Repo layout varies by app
- **Monorepo** (e.g. Varisankya, Pathivu): one repo with `android/`, `ios/`, `web/`. Gradle root
  is `android/`; run `./android/gradlew -p android ...` from the repo root, never `cd android`.
- **Outer-container / pre-monorepo** layout: a standalone `<app>-android` repo plus a sibling
  (uncommitted) `_tools/` directory for build tooling/secrets scripts.

Confirm `minSdk`, AGP/Kotlin versions, and R8 settings against the app's own
`gradle/libs.versions.toml` — see `hora-core/docs/conventions.md` for the latest known family
reference values.

## Steps

1. **Retrieve secrets.** Bitwarden is the source of truth — see `hora-bitwarden-secrets`. A
   per-app `retrieve_secrets.sh` typically writes `google-services.json`, the upload keystore,
   `play_console_key.json`, and signing creds into `local.properties`.
2. **Check the live versionCode before bumping.** The value in `build.gradle.kts` may already be
   published from a prior session. Check the Play Console UI, or attempt the publish — Play
   rejects "version code too low or already used" and implies the next free value.
3. **Bump `versionCode`** (keep `versionName` stable through beta, per the app's own scheme).
   Update the app's changelog/`CLAUDE.md` "current version" line and the Play release-notes file
   (≤ 500 chars, plain ASCII — em-dashes and curly quotes break the Play upload).
4. **Build the signed release + APK:** `bundleRelease` (Play) and `assembleRelease` (GitHub
   sideload). Signing reads `RELEASE_STORE_FILE/PASSWORD/KEY_ALIAS/KEY_PASSWORD` from gitignored
   `local.properties`.
5. **R8 sanity check (if minify is on):** confirm a green `minifyReleaseWithR8`. Model classes and
   any resource looked up via `getIdentifier` need explicit `-keep` rules or they silently break
   post-shrink.
6. **Security check — every release, non-negotiable:**
   ```bash
   git status                       # confirm none of: local.properties, *google-services.json,
                                     # *.jks/*.keystore, *-upload-key*, play_console_key.json, .env.local
   git add <files>                  # never `git add -A`
   git diff --cached --name-only    # re-verify after staging
   ```
7. **Commit + tag + push** to `main` (end the commit body with the `Co-Authored-By` line). Tag
   format and `versionName` scheme are per-app — check the wiki before assuming `v1.0-beta.N`.
8. **Cut the GitHub release** with the signed APK attached:
   `gh release create <tag> "<apk>#<Label>" --repo aarshps/<repo> --title "..." --notes "..." --prerelease`
9. **Upload to Play; pick the track by the app's gate status.** Play's 12-testers × 14-days rule
   is a ONE-TIME account/app unlock, not a per-release gate:
   - **Already past the gate / in production:** ship pre-releases straight to open Beta/Open
     Testing.
   - **New app/account, gate not cleared:** `publishReleaseBundle -PplayTrack=internal`; open
     testing/production wait for the one-time gate.
   - Verify the *live* track in Play Console or the wiki first — don't assume.
   - **Launch-day exception:** for an external/marketing launch, target Production with a direct
     link — "Join Beta → wait → install" friction hurts launch-day conversion.
   - "Connection reset" on upload is transient — retry. "version code too low/used" — bump +1,
     rebuild, re-commit, re-tag (delete the old tag/release first), redo from the build step.
10. **Promote lower tracks to stay current (optional, typical):**
    `promoteReleaseArtifact --from-track <src> --promote-track <dest> --release-status completed`.
11. **Update the wiki + repo docs in the same pass** — push the app's `.wiki` repo (`master`)
    alongside the step-7 commit, so docs never lag the shipped build.
12. **Update memory/project notes** with the shipped version and the next free versionCode.

## SECURITY — non-negotiable
Never stage/commit/print secrets. Gitignored: `local.properties`, `*google-services.json`,
`*.jks`/`*.keystore`, `*-upload-key*`, `play_console_key.json`, `.env.local`. Verify with
`git check-ignore` before staging, `git diff --cached --name-only` after. Each Hora app has its
own dedicated Firebase project — never shared.
