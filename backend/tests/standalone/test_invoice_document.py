import sys
from unittest.mock import MagicMock, patch
from datetime import date
from decimal import Decimal

# Aggressive mocking to prevent database connection on import
mock_db = MagicMock()
sys.modules["app.core.db"] = mock_db
sys.modules["app.core.security"] = MagicMock()

from app.services.document_service import generate_invoice_pdf, generate_invoice_html

def test_generate_invoice_pdf_success():
    """Verify that generate_invoice_pdf creates a PDF successfully."""
    # Mock RiskNote
    risk_note = MagicMock()
    risk_note.risk_note_number = "RN-001"
    risk_note.transaction_type.value = "New Business"
    risk_note.coverage_start = date(2025, 1, 1)
    risk_note.coverage_end = date(2025, 12, 31)
    risk_note.policy.policy_number = "POL-001"
    
    # Mock Line Item
    line_item = MagicMock()
    line_item.risk_note = risk_note
    line_item.amount = Decimal("10000.00")
    line_item.description = None
    
    # Mock Invoice
    invoice = MagicMock()
    invoice.invoice_number = "INV-001"
    invoice.date_issued = date(2025, 1, 1)
    invoice.due_date = date(2025, 2, 1)
    invoice.total_amount = Decimal("10000.00")
    invoice.balance_due = Decimal("10000.00")
    invoice.line_items = [line_item]
    
    # Mock Client
    client = MagicMock()
    client.name = "John Doe"
    client.kra_pin = "A123456789Z"
    
    # Execute PDF
    pdf_bytes = generate_invoice_pdf(invoice, client)
    
    # Assert PDF
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    assert pdf_bytes.startswith(b"%PDF-")

    # Execute HTML
    html_content = generate_invoice_html(invoice, client)
    
    # Assert HTML
    assert isinstance(html_content, str)
    assert "INV-001" in html_content
    assert "John Doe" in html_content
    assert "10,000.00" in html_content
