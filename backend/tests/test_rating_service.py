import pytest
from decimal import Decimal
from app.services.rating import RatingService
from app.models import Product
from app.schemas import MotorFinancialBreakdown

def test_motor_private_rating_logic():
    # Setup a mock or real product
    product = Product(
        name="Motor Private - Comprehensive",
        class_of_insurance="Motor Private",
        default_commission_rate=10.0
    )
    
    risk_details = {
        "VEHICLE DETAILS": {
            "Value Kshs.": 1000000.0, # 1M
        },
        "EXTENSIONS": {
            "pvt": True,
            "excess_protector": True
        }
    }
    
    # Expected math:
    # Basic Premium: 1M * 0.0325 = 32,500.00 (min 15,000)
    # PVT: 1M * 0.0025 = 2,500.00
    # Excess Protector: 1M * 0.0025 = 2,500.00
    # Net Premium: 32,500 + 2,500 + 2,500 = 37,500.00
    # Training Levy: 37,500 * 0.002 = 75.00
    # PHCF: 37,500 * 0.0025 = 93.75
    # Stamp Duty: 40.00
    # Total Levies: 75 + 93.75 + 40 = 208.75
    # Total Amount: 37,500 + 208.75 = 37,708.75
    
    breakdown = RatingService.calculate_breakdown(product, risk_details)
    
    assert isinstance(breakdown, MotorFinancialBreakdown)
    assert breakdown.net_premium == Decimal("37500.00")
    assert breakdown.taxes["training_levy"] == Decimal("75.00")
    assert breakdown.taxes["phcf"] == Decimal("93.75")
    assert breakdown.taxes["stamp_duty"] == Decimal("40.00")
    assert breakdown.total_amount == Decimal("37708.75")
    assert len(breakdown.benefits) == 2
