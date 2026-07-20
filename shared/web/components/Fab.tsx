"use client";

import type { ReactNode } from "react";

/**
 * Hora family extended FAB — the primary screen action: a leading icon + a short
 * label, in the `tertiary-container` colour (the family's dynamic-colour FAB
 * standard — softer, Material-You-driven tint vs. the more assertive primary
 * colour; matches every native app's `ExtendedFloatingActionButton.Tertiary`
 * style). The family standard is an **extended** (icon + label) FAB rather than
 * an icon-only circle, so the primary action is always self-describing. Pure UI.
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
      className={`fixed right-5 bottom-6 z-30 flex items-center gap-2 rounded-2xl bg-tertiary-container px-5 py-4 font-semibold text-on-tertiary-container shadow-lg transition hover:opacity-90 active:scale-95 ${className}`}
    >
      {icon}
      {label}
    </button>
  );
}
