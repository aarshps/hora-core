"use client";

import { ExternalLink } from "lucide-react";
import { Sheet } from "./Sheet";

/**
 * Hora family About sheet (presentational). Shows the app's identity (icon +
 * name + a small sub-label) and a short description, plus an optional list of
 * external legal links (Privacy / Data deletion). Prop-driven and free of
 * app-specific strings — each app supplies its own name, icon, copy, and links.
 *
 * Canonical in hora-core/shared/web/components/.
 */
export function AboutSheet({
  open,
  onClose,
  appName,
  description,
  iconSrc = "/icon-512.png",
  subLabel = "Web",
  links,
}: {
  open: boolean;
  onClose: () => void;
  appName: string;
  description: string;
  iconSrc?: string;
  subLabel?: string;
  links?: { label: string; href: string }[];
}) {
  return (
    <Sheet open={open} onClose={onClose} title={`About ${appName}`}>
      <div className="flex flex-col items-center gap-4 py-4 text-center">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={iconSrc}
          alt={appName}
          width={80}
          height={80}
          className="h-20 w-20 rounded-3xl"
        />
        <div>
          <p className="text-xl font-extrabold">{appName}</p>
          <p className="text-sm text-on-surface-variant">{subLabel}</p>
        </div>
        <p className="max-w-xs text-sm text-on-surface-variant">{description}</p>
      </div>
      {links && links.length > 0 && (
        <div className="flex flex-col">
          {links.map((l) => (
            <a
              key={l.href}
              href={l.href}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-3 border-t border-outline-variant/40 py-3 text-sm font-medium text-on-surface"
            >
              {l.label}
              <ExternalLink
                size={14}
                className="ml-auto text-on-surface-variant"
              />
            </a>
          ))}
        </div>
      )}
    </Sheet>
  );
}
