"use client";

import { useEffect, type ReactNode } from "react";
import { createPortal } from "react-dom";
import { X } from "lucide-react";

/**
 * Bottom-anchored modal sheet — the web counterpart of the native BottomSheet /
 * SwiftUI `.sheet`. Bottom sheet on mobile (32px top corners + drag handle),
 * centered rounded card on desktop. Dimmed scrim, scroll-locked body, slides up
 * on mount, Escape to close. Surface + top-corner shape come from the shared
 * `.sheet` utility (see web_shared.css).
 *
 * Hora family shared component — canonical in hora-core/shared/web/components/.
 */
export function Sheet({
  open,
  onClose,
  title,
  children,
  footer,
}: {
  open: boolean;
  onClose: () => void;
  title?: string;
  children: ReactNode;
  footer?: ReactNode;
}) {
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKey);
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = prev;
    };
  }, [open, onClose]);

  if (!open || typeof document === "undefined") return null;

  return createPortal(
    <div className="fixed inset-0 z-50 flex items-end justify-center sm:items-center">
      <div
        className="absolute inset-0 bg-black/40 animate-[hora-fade_0.2s_ease]"
        onClick={onClose}
        aria-hidden
      />
      <div
        role="dialog"
        aria-modal="true"
        aria-label={title}
        className="sheet relative flex max-h-[92vh] w-full flex-col shadow-2xl animate-[hora-slideup_0.28s_cubic-bezier(0.2,0.8,0.2,1)] sm:m-4 sm:max-w-lg sm:rounded-[28px]"
      >
        <div className="relative flex shrink-0 items-center gap-3 px-5 pt-4 pb-2">
          <div className="absolute left-1/2 top-2 h-1 w-9 -translate-x-1/2 rounded-full bg-on-surface-variant/30 sm:hidden" />
          {title && <h2 className="flex-1 text-lg font-bold">{title}</h2>}
          <button
            onClick={onClose}
            aria-label="Close"
            className="ml-auto grid h-9 w-9 place-items-center rounded-full text-on-surface-variant transition hover:bg-surface-container active:scale-95"
          >
            <X size={20} />
          </button>
        </div>
        <div className="no-scrollbar flex-1 overflow-y-auto px-5 pb-5">{children}</div>
        {footer && (
          <div className="shrink-0 border-t border-outline-variant/40 p-4">{footer}</div>
        )}
      </div>
      <style>{`
        @keyframes hora-slideup { from { transform: translateY(100%); } to { transform: translateY(0); } }
        @keyframes hora-fade { from { opacity: 0; } to { opacity: 1; } }
      `}</style>
    </div>,
    document.body,
  );
}
