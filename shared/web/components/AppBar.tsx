"use client";

import type { ReactNode } from "react";

/**
 * Hora family home top app-bar — a sticky bar with a leading slot (the profile /
 * avatar button), a **centered** title, and a trailing actions slot. The family
 * standard is a centered title, balanced by the leading + action buttons. Pure
 * UI; the caller supplies the leading/actions content.
 *
 * Canonical in hora-core/shared/web/components/.
 */
export function AppBar({
  leading,
  title,
  actions,
  className = "",
}: {
  leading?: ReactNode;
  title: string;
  actions?: ReactNode;
  className?: string;
}) {
  return (
    <header
      className={`sticky top-0 z-20 -mx-4 mb-2 flex items-center gap-2 bg-bg px-4 py-3 ${className}`}
    >
      {leading}
      <h1 className="flex-1 text-center text-2xl font-extrabold tracking-tight">
        {title}
      </h1>
      {actions}
    </header>
  );
}
