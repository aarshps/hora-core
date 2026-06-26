"use client";

import type { ButtonHTMLAttributes, ReactNode } from "react";
import { ChevronDown } from "lucide-react";

/**
 * Hora family shared form controls — Material 3 Expressive, role-token themed.
 * Canonical in hora-core/shared/web/components/. Pure UI; no app-specific logic.
 */

export function Button({
  variant = "primary",
  className = "",
  children,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "tonal" | "ghost" | "danger" | "outline";
}) {
  // Material 3 button styles (filled / tonal / outlined / text / destructive),
  // pill-shaped to match Android's ShapeAppearance.App.Button.
  const base =
    "inline-flex items-center justify-center gap-2 rounded-full px-6 py-2.5 text-sm font-semibold tracking-[0.01em] transition disabled:opacity-50 disabled:pointer-events-none";
  const styles: Record<string, string> = {
    primary: "bg-primary text-on-primary hover:opacity-90 active:opacity-100",
    tonal: "bg-secondary-container text-on-secondary-container hover:opacity-90",
    outline: "border border-outline-strong text-primary hover:bg-primary/10",
    ghost: "text-primary hover:bg-primary/10",
    danger: "border border-error text-error hover:bg-error/10",
  };
  return (
    <button className={`${base} ${styles[variant]} ${className}`} {...props}>
      {children}
    </button>
  );
}

export function Switch({
  checked,
  onChange,
  disabled,
}: {
  checked: boolean;
  onChange: (v: boolean) => void;
  disabled?: boolean;
}) {
  // Material 3 switch. The off-state track uses a filled container + visible
  // outline so it reads clearly in dark mode (a bg-outline track is nearly
  // invisible on a dark surface); the thumb grows when on.
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      disabled={disabled}
      onClick={() => onChange(!checked)}
      className={`relative h-7 w-12 shrink-0 rounded-full border-2 transition-colors disabled:opacity-40 ${
        checked ? "border-primary bg-primary" : "border-outline-strong bg-surface-3"
      }`}
    >
      <span
        className={`absolute top-1/2 -translate-y-1/2 rounded-full transition-all ${
          checked ? "right-1 h-5 w-5 bg-on-primary" : "left-1 h-4 w-4 bg-outline-strong"
        }`}
      />
    </button>
  );
}

export function Field({
  label,
  children,
}: {
  label: string;
  children: ReactNode;
}) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-xs font-semibold text-on-surface-variant">
        {label}
      </span>
      {children}
    </label>
  );
}

// M3 outlined input: visible outline, primary focus ring, theme-aware native
// controls (color-scheme is set globally so the date picker indicator adapts).
const inputClass =
  "w-full min-w-0 rounded-lg border border-outline-strong bg-surface-2 px-4 py-3 text-base text-on-surface outline-none transition focus:border-primary focus:ring-1 focus:ring-primary";

export function TextInput(props: React.InputHTMLAttributes<HTMLInputElement>) {
  return <input {...props} className={`${inputClass} ${props.className ?? ""}`} />;
}

export function Select({
  className = "",
  children,
  ...props
}: React.SelectHTMLAttributes<HTMLSelectElement> & { children: ReactNode }) {
  // The native dropdown arrow sits flush to the edge and looks cramped (worse
  // with rounded corners and in dark mode). Hide it and render our own chevron,
  // properly inset and theme-coloured. The wrapper carries layout classes
  // (w-40 / flex-1); the select fills it.
  return (
    <div className={`relative ${className}`}>
      <select {...props} className={`${inputClass} cursor-pointer appearance-none pr-10`}>
        {children}
      </select>
      <ChevronDown
        size={18}
        aria-hidden
        className="pointer-events-none absolute top-1/2 right-3 -translate-y-1/2 text-on-surface-variant"
      />
    </div>
  );
}

export function Segmented<T extends string>({
  options,
  selected,
  onSelect,
  className = "",
}: {
  options: { value: T; label: string }[];
  selected: T;
  onSelect: (v: T) => void;
  className?: string;
}) {
  // M3 segmented selector — pill track, filled-primary active segment. The web
  // counterpart of Android's ChipGroup single-selection / the iOS segmented control.
  return (
    <div className={`flex gap-1 rounded-full bg-surface-container p-1 ${className}`}>
      {options.map((o) => {
        const on = o.value === selected;
        return (
          <button
            key={o.value}
            type="button"
            onClick={() => onSelect(o.value)}
            className={`flex-1 rounded-full px-3 py-1.5 text-sm font-semibold transition ${
              on ? "bg-primary text-on-primary" : "text-on-surface-variant"
            }`}
          >
            {o.label}
          </button>
        );
      })}
    </div>
  );
}
