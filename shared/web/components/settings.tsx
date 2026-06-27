"use client";

import type { ReactNode } from "react";
import { Switch } from "./controls";

/**
 * Hora family settings design language — the building blocks every app's
 * Settings screen is assembled from. Pure layout primitives, role-token themed,
 * free of app-specific logic. Canonical in hora-core/shared/web/components/.
 */

/** A grouped settings card (the shared `.card` surface) with an optional label. */
export function SettingsSection({
  title,
  children,
}: {
  title?: string;
  children: ReactNode;
}) {
  return (
    <section className="card mb-3 p-4">
      {title && <SettingsSectionLabel>{title}</SettingsSectionLabel>}
      {children}
    </section>
  );
}

/** The small uppercase section heading inside a card. */
export function SettingsSectionLabel({ children }: { children: ReactNode }) {
  return (
    <p className="text-xs font-bold uppercase tracking-wide text-on-surface-variant">
      {children}
    </p>
  );
}

/** A label (+ optional sub-label) on the left, a control slot on the right. */
export function SettingsRow({
  label,
  sub,
  children,
}: {
  label: string;
  sub?: string;
  children?: ReactNode;
}) {
  return (
    <div className="flex items-center justify-between gap-3 py-1">
      <div className="min-w-0">
        <p className="font-semibold">{label}</p>
        {sub && <p className="text-xs text-on-surface-variant">{sub}</p>}
      </div>
      {children}
    </div>
  );
}

/** A `SettingsRow` whose control is the shared M3 `Switch`. */
export function SettingsToggle({
  label,
  sub,
  checked,
  onChange,
}: {
  label: string;
  sub?: string;
  checked: boolean;
  onChange: (v: boolean) => void;
}) {
  return (
    <SettingsRow label={label} sub={sub}>
      <Switch checked={checked} onChange={onChange} />
    </SettingsRow>
  );
}

/** A hairline divider between rows inside a card. */
export function SettingsDivider() {
  return <div className="my-2 h-px bg-outline/60" />;
}

/**
 * A tappable row — leading icon, label, trailing affordance. Renders an external
 * `<a>` when `href` is set, otherwise a `<button>` calling `onClick` (e.g. to open
 * an About sheet). Icons + trailing are passed in so this stays icon-set agnostic.
 */
export function SettingsLinkRow({
  icon,
  label,
  href,
  onClick,
  trailing,
}: {
  icon?: ReactNode;
  label: string;
  href?: string;
  onClick?: () => void;
  trailing?: ReactNode;
}) {
  const cls =
    "flex w-full items-center gap-3 py-3 text-left font-medium text-on-surface";
  const body = (
    <>
      {icon}
      <span className="flex-1">{label}</span>
      {trailing}
    </>
  );
  if (href) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer" className={cls}>
        {body}
      </a>
    );
  }
  return (
    <button onClick={onClick} className={cls}>
      {body}
    </button>
  );
}
