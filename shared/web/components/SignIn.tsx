"use client";

import { useState, type ReactNode } from "react";
import { Button } from "./controls";

/**
 * Hora family sign-in shell (presentational). Google-only — the same accounts as
 * the native apps, so the user's data appears instantly. The auth wiring is
 * supplied by the caller via `onSignIn`, so each app keeps its own auth +
 * analytics layer (this component stays free of app-specific logic).
 *
 * Canonical in hora-core/shared/web/components/.
 */
export function SignIn({
  appName,
  tagline,
  iconSrc = "/icon-512.png",
  onSignIn,
  externalError,
  footer,
}: {
  appName: string;
  tagline: string;
  iconSrc?: string;
  onSignIn: () => Promise<void>;
  /** An error surfaced out of band (e.g. from a redirect round-trip). */
  externalError?: string | null;
  footer?: ReactNode;
}) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function go() {
    setBusy(true);
    setError(null);
    try {
      // On the redirect path the page navigates away here; on the popup path a
      // resolved promise means onAuthStateChanged swaps this screen out.
      await onSignIn();
    } catch (e) {
      setError((e as Error)?.message ?? "Sign-in failed — please try again.");
      setBusy(false);
    }
  }

  const shownError = error ?? externalError ?? null;

  return (
    <main className="flex min-h-dvh flex-col items-center justify-center px-6">
      <div className="flex w-full max-w-sm flex-col items-center gap-6 rounded-3xl border border-outline bg-surface px-8 py-12 text-center shadow-sm">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={iconSrc}
          alt={appName}
          width={96}
          height={96}
          className="h-24 w-24 rounded-3xl"
        />
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight">{appName}</h1>
          <p className="mt-2 text-sm text-on-surface-variant">{tagline}</p>
        </div>
        <Button onClick={go} disabled={busy} className="w-full">
          <GoogleMark />
          {busy ? "Signing in…" : "Continue with Google"}
        </Button>
        {shownError && <p className="text-sm text-error">{shownError}</p>}
        {footer}
      </div>
    </main>
  );
}

function GoogleMark() {
  return (
    <svg width="18" height="18" viewBox="0 0 48 48" aria-hidden>
      <path
        fill="#FFC107"
        d="M43.6 20.5H42V20H24v8h11.3C33.7 32.9 29.3 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34.3 6.1 29.4 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.3-.4-3.5z"
      />
      <path
        fill="#FF3D00"
        d="m6.3 14.7 6.6 4.8C14.7 16 19 13 24 13c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34.3 6.1 29.4 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"
      />
      <path
        fill="#4CAF50"
        d="M24 44c5.2 0 10-2 13.6-5.2l-6.3-5.3C29.2 35 26.7 36 24 36c-5.3 0-9.7-3.1-11.3-7.6l-6.5 5C9.6 39.6 16.2 44 24 44z"
      />
      <path
        fill="#1976D2"
        d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.1-4 5.5l6.3 5.3C41.4 36.5 44 30.8 44 24c0-1.3-.1-2.3-.4-3.5z"
      />
    </svg>
  );
}
