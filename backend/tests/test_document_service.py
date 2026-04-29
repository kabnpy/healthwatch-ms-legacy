from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from app.services.document_service import generate_risknote_pdf


# Mock the db fixture to avoid database connection issues in this test
@pytest.fixture(scope="session", autouse=True)
def db():
    return MagicMock()


def test_generate_risknote_pdf_success():
    """Verify that generate_risknote_pdf creates a PDF successfully."""
    # Mock RiskNote
    risk_note = MagicMock()
    risk_note.risk_note_number = "RN-001"
    risk_note.status = "Final"
    risk_note.coverage_start = datetime(2025, 1, 1)
    risk_note.coverage_end = datetime(2025, 12, 31)
    risk_note.created_at = datetime(2025, 1, 1)
    risk_note.net_premium = Decimal("10000.00")
    risk_note.total_amount = Decimal("12000.00")
    risk_note.financial_breakdown = {
        "benefits": [{"name": "P.V.T", "amount": 1000}],
        "taxes": {"Training_Levy": 100},
    }
    risk_note.cover_snapshot = {
        "VEHICLE": {"Reg. No": "KBA 123A", "Make": "Toyota"},
        "sum_insured": 500000,
    }

    # Mock Client
    client = MagicMock()
    client.name = "John Doe"
    client.kra_pin = "A123456789Z"
    client.physical_address = "Bishop Tower"
    client.postal_number = "123"
    client.postal_code = "00100"
    client.town = "Nairobi"

    # Mock Policy/Product
    policy = MagicMock()
    policy.policy_number = "POL-001"
    policy.product.name = "Motor Private"
    policy.product.class_of_insurance = "Motor"
    policy.product.product_details = {
        "VEHICLE": {"Reg. No": "KBA 000X", "Value Kshs.": 0}
    }
    policy.product.insurer.name = "AIG"

    # Execute
    pdf_bytes = generate_risknote_pdf(risk_note, client, policy)

    # Assert
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    # Basic check for PDF magic number %PDF-
    assert pdf_bytes.startswith(b"%PDF-")


if __name__ == "__main__":
    pytest.main([__file__])
