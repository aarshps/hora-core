"use client";

import type { ReactNode } from "react";

/**
 * Hora family empty-state card — a centered icon disc, title, description, and an
 * optional call-to-action. Prop-driven and string-free; the caller supplies the
 * icon node + copy. Canonical in hora-core/shared/web/components/.
 */
export function EmptyState({
  icon,
  title,
  description,
  actionLabel,
  onAction,
}: {
  icon: ReactNode;
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
}) {
  return (
    <div className="card flex flex-col items-center gap-4 px-6 py-16 text-center">
      <div className="flex h-16 w-16 items-center justify-center rounded-3xl bg-surface-2">
        {icon}
      </div>
      <div>
        <p className="text-lg font-bold">{title}</p>
        <p className="mt-1 text-sm text-on-surface-variant">{description}</p>
      </div>
      {actionLabel && onAction && (
        <button
          onClick={onAction}
          className="rounded-full bg-primary px-6 py-2.5 font-semibold text-on-primary"
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
}
