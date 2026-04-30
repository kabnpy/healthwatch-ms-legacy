from typing import cast

from app.models import RiskNote


class RiskNoteService:
    @staticmethod
    def get_special_clauses(risk_note: RiskNote) -> list[str]:
        """
        Extract special clauses from cover snapshot or raw field.
        """
        snapshot_terms = risk_note.cover_snapshot.get("terms", {})
        if isinstance(snapshot_terms, dict):
            snapshot_clauses = snapshot_terms.get("special_clauses")
            if snapshot_clauses:
                if isinstance(snapshot_clauses, str):
                    return [snapshot_clauses]
                return cast(list[str], snapshot_clauses)
        return risk_note.special_clauses_raw

    @staticmethod
    def get_invoice_number(risk_note: RiskNote) -> str | None:
        """
        Get the associated invoice number for this risk note.
        """
        if risk_note.invoice_line_items and risk_note.invoice_line_items[0].invoice:
            return risk_note.invoice_line_items[0].invoice.invoice_number
        return None


risknote_service = RiskNoteService()
