"use client";

import type { ReactNode } from "react";
import { ArrowLeft } from "lucide-react";

/**
 * Hora family screen header — a sticky top app-bar for secondary screens: a back
 * button, a title, and an optional trailing slot (actions / view toggle). Pure
 * UI; the caller owns navigation via `onBack` (e.g. close an overlay, or
 * `router.push("/")` on a routed screen). `centered` centers the title and adds
 * a spacer to balance the back button when there is no trailing content.
 *
 * Canonical in hora-core/shared/web/components/.
 */
export function ScreenHeader({
  title,
  onBack,
  trailing,
  centered = false,
  className = "",
}: {
  title: string;
  onBack: () => void;
  trailing?: ReactNode;
  centered?: boolean;
  className?: string;
}) {
  return (
    <header
      className={`sticky top-0 z-10 flex items-center gap-3 bg-bg px-4 py-3 ${className}`}
    >
      <button
        onClick={onBack}
        aria-label="Back"
        className="rounded-full p-2 transition hover:bg-black/5 dark:hover:bg-white/10"
      >
        <ArrowLeft size={20} />
      </button>
      <h1
        className={`flex-1 text-xl font-extrabold${centered ? " text-center" : ""}`}
      >
        {title}
      </h1>
      {trailing ?? (centered ? <span className="w-9" /> : null)}
    </header>
  );
}
