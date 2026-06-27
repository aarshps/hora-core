"use client";

import type { ReactNode } from "react";

/**
 * Hora family extended FAB — the primary screen action: a leading icon + a short
 * label, in the `primary-container` colour, fixed bottom-right. The family
 * standard is an **extended** (icon + label) FAB rather than an icon-only circle,
 * so the primary action is always self-describing. Pure UI.
 *
 * Canonical in hora-core/shared/web/components/.
 */
export function Fab({
  icon,
  label,
  onClick,
  className = "",
}: {
  icon: ReactNode;
  label: string;
  onClick: () => void;
  className?: string;
}) {
  return (
    <button
      onClick={onClick}
      className={`fixed right-5 bottom-6 z-30 flex items-center gap-2 rounded-2xl bg-primary-container px-5 py-4 font-semibold text-on-primary-container shadow-lg transition hover:opacity-90 active:scale-95 ${className}`}
    >
      {icon}
      {label}
    </button>
  );
}
