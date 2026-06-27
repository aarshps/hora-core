"use client";

import { Sheet } from "./Sheet";
import { Button } from "./controls";

/**
 * Hora family confirmation dialog — a small `Sheet` with a message and a
 * Cancel / confirm button pair. `danger` swaps the confirm button to the
 * destructive variant; `busy` disables it and shows a working label. Pure UI,
 * prop-driven — the caller owns the action and the open/close state.
 *
 * Canonical in hora-core/shared/web/components/.
 */
export function ConfirmDialog({
  open,
  title,
  message,
  confirmLabel = "Confirm",
  danger = false,
  busy = false,
  onConfirm,
  onClose,
}: {
  open: boolean;
  title: string;
  message: string;
  confirmLabel?: string;
  danger?: boolean;
  busy?: boolean;
  onConfirm: () => void;
  onClose: () => void;
}) {
  return (
    <Sheet
      open={open}
      onClose={onClose}
      title={title}
      footer={
        <div className="flex gap-3">
          <Button variant="ghost" className="flex-1" onClick={onClose}>
            Cancel
          </Button>
          <Button
            variant={danger ? "danger" : "primary"}
            className="flex-1"
            onClick={onConfirm}
            disabled={busy}
          >
            {busy ? "Working…" : confirmLabel}
          </Button>
        </div>
      }
    >
      <p className="py-2 text-sm text-on-surface-variant">{message}</p>
    </Sheet>
  );
}
