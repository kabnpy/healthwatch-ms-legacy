import os
from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock
from app.services.document_service import generate_risknote_pdf

def test_generate_risknote_visual_verification():
    """
    Generates a Risk Note PDF and saves it to a temporary file for visual verification.
    This helps in verifying the layout changes as we update the template.
    """
    # Mock RiskNote
    risk_note = MagicMock()
    risk_note.risk_note_number = "RN-2026-03-19"
    risk_note.status = "Final"
    risk_note.coverage_start = datetime(2025, 7, 27)
    risk_note.coverage_end = datetime(2026, 7, 26)
    risk_note.created_at = datetime(2026, 3, 16)
    risk_note.net_premium = Decimal("50500.00")
    risk_note.total_amount = Decimal("61370.00")
    risk_note.financial_breakdown = {
        "benefits": [
            {"name": "Excess Waiver", "amount": 5050.00},
            {"name": "PVT", "amount": 4545.00},
            {"name": "PLL", "amount": 1000.00}
        ],
        "taxes": {
            "Training_Levy": 122.00,
            "PHCF_Levy": 153.00
        }
    }
    risk_note.cover_snapshot = {
        "VEHICLE": {
            "Reg No": "KDH 519E",
            "Make": "Toyota Hilux",
            "Year": "2020",
        },
        "sum_insured": Decimal("2700000.00")
    }
    
    # Mock Client
    client = MagicMock()
    client.name = "John Doe"
    client.kra_pin = "1234567890"
    client.physical_address = "P.O.BOX 12345 - 678"
    client.postal_number = "12345"
    client.postal_code = "678"
    client.town = "Nairobi"
    
    # Mock Policy/Product
    policy = MagicMock()
    policy.policy_number = "010/030/1/004071/2000"
    policy.product.name = "Motor Private"
    policy.product.class_of_insurance = "Motor"
    policy.product.product_details = {
        "VEHICLE": {"Reg No": "", "Make": "", "Year": "", "Value Kshs.": 0}
    }
    policy.product.insurer.name = "Old Mutual General Insurance (K) Ltd"
    
    # Execute
    pdf_bytes = generate_risknote_pdf(risk_note, client, policy)
    
    # Save to file
    output_path = os.path.join(os.getcwd(), "risknote_test_output.pdf")
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)
    
    print(f"\n[INFO] Risk Note PDF generated and saved to: {output_path}")
    assert os.path.exists(output_path)
    assert len(pdf_bytes) > 0

if __name__ == "__main__":
    test_generate_risknote_visual_verification()
