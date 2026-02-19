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
    
    # Expected math (NEW TIERS):
    # Tier for 1M: 5.0%, min 60,000
    # Basic Premium: 1M * 0.05 = 50,000.00 -> Min applied: 60,000.00
    # PVT: 1M * 0.0025 = 2,500.00
    # Excess Protector: 1M * 0.0025 = 2,500.00
    # Net Premium: 60,000 + 2,500 + 2,500 = 65,000.00
    # Training Levy: 65,000 * 0.002 = 130.00
    # PHCF: 65,000 * 0.0025 = 162.50
    # Stamp Duty: 40.00
    # Total Levies: 130 + 162.50 + 40 = 332.50
    # Total Amount: 65,000 + 332.50 = 65,332.50
    
    breakdown = RatingService.calculate_breakdown(product, risk_details)
    
    assert isinstance(breakdown, MotorFinancialBreakdown)
    assert breakdown.net_premium == Decimal("65000.00")
    assert breakdown.taxes["training_levy"] == Decimal("130.00")
    assert breakdown.taxes["phcf"] == Decimal("162.50")
    assert breakdown.taxes["stamp_duty"] == Decimal("40.00")
    assert breakdown.total_amount == Decimal("65332.50")
    assert len(breakdown.benefits) == 2

def test_motor_private_om_rescue_plus():
    product = Product(
        name="Motor Private - Comprehensive",
        class_of_insurance="Motor Private",
        default_commission_rate=10.0
    )
    
    risk_details = {
        "VEHICLE DETAILS": {
            "Value Kshs.": 1000000.0,
        },
        "EXTENSIONS": {
            "om_rescue_plus": True
        }
    }
    
    # Basic: 60,000.00 (min)
    # Net: 60,000.00
    # Levies on 60,000:
    #   Training: 60,000 * 0.002 = 120.00
    #   PHCF: 60,000 * 0.0025 = 150.00
    #   Stamp Duty: 40.00
    # Total Levies: 120 + 150 + 40 = 310.00
    # OM Rescue Plus (post-levy): 1,000.00
    # Total: 60,000 + 310.00 + 1,000 = 61,310.00
    
    breakdown = RatingService.calculate_breakdown(product, risk_details)
    
    assert breakdown.net_premium == Decimal("60000.00")
    assert breakdown.taxes["training_levy"] == Decimal("120.00")
    assert breakdown.taxes["phcf"] == Decimal("150.00")
    assert breakdown.total_amount == Decimal("61310.00")
    assert any(b.name == "OM Rescue Plus" for b in breakdown.benefits)

def test_motor_private_high_end_inclusive():
    product = Product(
        name="Motor Private - Comprehensive",
        class_of_insurance="Motor Private",
        default_commission_rate=10.0
    )
    
    risk_details = {
        "VEHICLE DETAILS": {
            "Value Kshs.": 4000000.0, # 4M
        },
        "EXTENSIONS": {
            "pvt": True,
            "excess_protector": True
        }
    }
    
    # Expected math:
    # Tier for 4M: 3.25%, min 0
    # Basic Premium: 4M * 0.0325 = 130,000.00
    # PVT (High End Inclusive): 0.00
    # Excess Protector (High End Inclusive): 0.00
    # Net Premium: 130,000.00
    # Training Levy: 130,000 * 0.002 = 260.00
    # PHCF: 130,000 * 0.0025 = 325.00
    # Stamp Duty: 40.00
    # Total Amount: 130,000 + 260 + 325 + 40 = 130,625.00
    
    breakdown = RatingService.calculate_breakdown(product, risk_details)
    
    assert breakdown.is_high_end is True
    assert breakdown.net_premium == Decimal("130000.00")
    assert breakdown.total_amount == Decimal("130625.00")
    # Benefits exist but are 0.00
    pvt = next(b for b in breakdown.benefits if b.name == "PVT")
    assert pvt.amount == Decimal("0.00")

def test_rating_service_robust_parsing():
    product = Product(
        name="Motor Private - Comprehensive",
        class_of_insurance="Motor Private",
        default_commission_rate=10.0
    )
    
    # Test with formatted currency string
    risk_details_formatted = {
        "VEHICLE DETAILS": {
            "Value Kshs.": "1,500,000.00",
        }
    }
    
    # 1.5M * 0.05 = 75,000.00 (min 60,000) -> 75,000.00
    # Net: 75,000.00
    # Levies on 75,000:
    #   Training: 75,000 * 0.002 = 150.00
    #   PHCF: 75,000 * 0.0025 = 187.50
    #   Stamp Duty: 40.00
    # Total: 75,000 + 150 + 187.50 + 40 = 75,377.50
    
    breakdown = RatingService.calculate_breakdown(product, risk_details_formatted)
    assert breakdown.net_premium == Decimal("75000.00")
    assert breakdown.total_amount == Decimal("75377.50")

    # Test with empty placeholder
    risk_details_empty = {
        "VEHICLE DETAILS": {
            "Value Kshs.": "[ EMPTY ]",
        }
    }
    breakdown = RatingService.calculate_breakdown(product, risk_details_empty)
    # Value is 0, so basic premium is 0, but min is 60,000 or some other logic
    # Looking at tiers: for 0 < 1.5M, rate is 0.05, min is 60,000.
    assert breakdown.net_premium == Decimal("60000.00")

    # Test with other non-numeric characters
    risk_details_dirty = {
        "VEHICLE DETAILS": {
            "Value Kshs.": "KES 2,000,000.00",
        }
    }
    
    # 2M * 0.04 = 80,000.00 (min 75,000) -> 80,000.00
    # Levies: 160 + 200 + 40 = 400.00
    # Total: 80,000 + 400 = 80,400.00
    breakdown = RatingService.calculate_breakdown(product, risk_details_dirty)
    assert breakdown.net_premium == Decimal("80000.00")
    assert breakdown.total_amount == Decimal("80400.00")

