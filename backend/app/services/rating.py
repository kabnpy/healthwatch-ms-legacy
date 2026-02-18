from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Protocol
from app.models import Product
from app.schemas import MotorFinancialBreakdown, BaseFinancialBreakdown, BenefitLineItem, FinancialBreakdown

class RatingStrategy(ABC):
    @abstractmethod
    def calculate(self, product: Product, risk_details: dict[str, Any]) -> BaseFinancialBreakdown | MotorFinancialBreakdown:
        pass

class MotorPrivateRatingStrategy(RatingStrategy):
    def calculate(self, product: Product, risk_details: dict[str, Any]) -> MotorFinancialBreakdown:
        risk_data = risk_details.get("VEHICLE DETAILS", risk_details)
        value = Decimal(str(risk_data.get("Value Kshs.", 0)))
        
        # 1. Basic Premium
        basic_rate = Decimal("0.0325")
        basic_premium = (value * basic_rate).quantize(Decimal("0.01"))
        basic_premium = max(Decimal("15000.00"), basic_premium)
        
        # 2. Extensions / Benefits
        extensions = risk_details.get("EXTENSIONS", {})
        benefits = []
        
        net_premium = basic_premium
        
        if extensions.get("pvt"):
            pvt_amount = (value * Decimal("0.0025")).quantize(Decimal("0.01"))
            benefits.append(BenefitLineItem(name="PVT", amount=pvt_amount))
            net_premium += pvt_amount
            
        if extensions.get("excess_protector"):
            ep_amount = (value * Decimal("0.0025")).quantize(Decimal("0.01"))
            benefits.append(BenefitLineItem(name="Excess Protector", amount=ep_amount))
            net_premium += ep_amount
            
        # 3. Levies
        levies = self._calculate_standard_levies(net_premium)
        total_levies = sum(levies.values())
        
        # 4. Post-Levy Benefits (e.g., OM Rescue Plus)
        post_levy_total = Decimal("0.00")
        if extensions.get("om_rescue_plus") or extensions.get("omRescuePlus"):
            om_amount = Decimal("1000.00")
            benefits.append(BenefitLineItem(name="OM Rescue Plus", amount=om_amount))
            post_levy_total += om_amount

        # 5. Commission
        commission_rate = Decimal(str(product.default_commission_rate / 100))
        commission_amount = (net_premium * commission_rate).quantize(Decimal("0.01"))
        
        return MotorFinancialBreakdown(
            type="motor",
            net_premium=net_premium,
            taxes=levies,
            commission_amount=commission_amount,
            total_amount=net_premium + total_levies + post_levy_total,
            benefits=benefits
        )

    def _calculate_standard_levies(self, net_premium: Decimal) -> dict[str, Decimal]:
        training_levy = (net_premium * Decimal("0.002")).quantize(Decimal("0.01"))
        phcf = (net_premium * Decimal("0.0025")).quantize(Decimal("0.01"))
        stamp_duty = Decimal("40.00")
        
        return {
            "training_levy": training_levy,
            "phcf": phcf,
            "stamp_duty": stamp_duty
        }

class RatingService:
    _strategies: dict[str, RatingStrategy] = {
        "motor private": MotorPrivateRatingStrategy()
    }

    @classmethod
    def calculate_levies(cls, net_premium: Decimal) -> dict[str, Decimal]:
        # Uses the standard Kenyan levies logic
        strategy = MotorPrivateRatingStrategy() # Both currently use same levies
        return strategy._calculate_standard_levies(net_premium)

    @classmethod
    def calculate_breakdown(cls, product: Product, risk_details: dict[str, Any]) -> BaseFinancialBreakdown | MotorFinancialBreakdown:
        class_of_insurance = product.class_of_insurance.lower()
        
        strategy = None
        for key, s in cls._strategies.items():
            if key in class_of_insurance:
                strategy = s
                break
        
        if not strategy:
            # Fallback or generic strategy
            return cls._calculate_generic(product, risk_details)
            
        return strategy.calculate(product, risk_details)

    @classmethod
    def _calculate_generic(cls, product: Product, risk_details: dict[str, Any]) -> BaseFinancialBreakdown:
        # Placeholder for other products
        net_premium = Decimal("0.00")
        training_levy = Decimal("0.00")
        phcf = Decimal("0.00")
        stamp_duty = Decimal("40.00")
        
        return BaseFinancialBreakdown(
            type="base",
            net_premium=net_premium,
            taxes={"stamp_duty": stamp_duty},
            commission_amount=Decimal("0.00"),
            total_amount=net_premium + stamp_duty
        )
