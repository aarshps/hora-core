# Templates

Starting-point files for a new Hora app's `shared/` contract folder. These are
**copy-and-customize** templates, not a runtime dependency — there is nothing to
import or link against. Copy the relevant subfolder into the new app's `shared/`,
then edit the placeholders for that app's actual collections and Firebase project.

- `shared-firebase/` — `firebase.json` + a `firestore.rules` skeleton implementing the
  family's per-user-ownership convention (see `docs/conventions.md` → "Firebase
  contract folder").

Not templated here: `shared/domain/SPEC.md` and `golden-vectors.json`. Those encode
each app's actual business logic and data shape, so there's no useful boilerplate to
copy — only the *methodology* is shared (see `docs/conventions.md` → "Domain spec +
golden-vector parity testing").
