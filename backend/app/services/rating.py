from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any

from app.models import Product
from app.schemas import (
    BenefitLineItem,
    MotorFinancialBreakdown,
)


class RatingStrategy(ABC):
    @abstractmethod
    def calculate(
        self, product: Product, risk_details: dict[str, Any]
    ) -> MotorFinancialBreakdown:
        pass

    @staticmethod
    def parse_decimal(value: Any) -> Decimal:
        """
        Robustly parse a value into a Decimal.
        """
        from app.utils import parse_decimal

        return parse_decimal(value)

    def _calculate_standard_levies(self, net_premium: Decimal) -> dict[str, Decimal]:
        return {
            "training_levy": (net_premium * Decimal("0.002")).quantize(Decimal("0.01")),
            "phcf": (net_premium * Decimal("0.0025")).quantize(Decimal("0.01")),
            "stamp_duty": Decimal("40.00"),
        }


class MotorPrivateRatingStrategy(RatingStrategy):
    DEFAULT_TIERS = [
        {"max": Decimal("1500000"), "rate": Decimal("0.05"), "min": Decimal("60000")},
        {"max": Decimal("2500000"), "rate": Decimal("0.04"), "min": Decimal("75000")},
        {"max": Decimal("3000000"), "rate": Decimal("0.035"), "min": Decimal("100000")},
        {"max": Decimal("5000000"), "rate": Decimal("0.0325"), "min": Decimal("0")},
        {"max": Decimal("Infinity"), "rate": Decimal("0.03"), "min": Decimal("0")},
    ]

    def calculate(
        self, product: Product, risk_details: dict[str, Any]
    ) -> MotorFinancialBreakdown:
        vehicle = risk_details.get("vehicle") or risk_details.get("vehicle_details", {})
        value = RatingStrategy.parse_decimal(vehicle.get("sum_insured", 0))

        # Allow zero value, will use minimum premium from the applicable tier

        product_tiers = product.pricing_rules.get("tiers")
        if product_tiers:
            tiers = []
            for t in product_tiers:
                tiers.append(
                    {
                        "max": Decimal(str(t["max"]))
                        if t["max"] is not None
                        else Decimal("Infinity"),
                        "rate": Decimal(str(t["rate"])) / Decimal("100"),
                        "min": Decimal(str(t.get("min", 0))),
                    }
                )
            # Tiers should ideally be stored sorted, but we ensure sorting here once.
            tiers.sort(key=lambda x: x["max"])
        else:
            tiers = self.DEFAULT_TIERS

        applicable_tier = next((t for t in tiers if value <= t["max"]), tiers[-1])
        basic_rate = applicable_tier["rate"]
        basic_premium = max(
            applicable_tier["min"], (value * basic_rate).quantize(Decimal("0.01"))
        )

        extensions = risk_details.get("extensions") or risk_details.get(
            "added_benefits", {}
        )
        benefits = []
        net_premium = basic_premium
        high_end_threshold = Decimal(
            str(product.pricing_rules.get("high_end_threshold", "3000000"))
        )
        is_high_end = value >= high_end_threshold

        # Benefits logic
        for ext, rate, name in [
            ("pvt", Decimal("0.0025"), "PVT"),
            ("excess_protector", Decimal("0.0025"), "Excess Protector"),
        ]:
            if extensions.get(ext):
                amount = (
                    Decimal("0.00")
                    if is_high_end
                    else (value * rate).quantize(Decimal("0.01"))
                )
                benefits.append(BenefitLineItem(name=name, amount=amount))
                net_premium += amount

        if extensions.get("passenger_liability"):
            pl_amount = Decimal("500.00")
            benefits.append(
                BenefitLineItem(name="Passenger Liability", amount=pl_amount)
            )
            net_premium += pl_amount

        levies = self._calculate_standard_levies(net_premium)
        total_levies = sum(levies.values())

        post_levy_total = Decimal("0.00")
        if extensions.get("om_rescue_plus"):
            om_amount = Decimal("1000.00")
            benefits.append(BenefitLineItem(name="OM Rescue Plus", amount=om_amount))
            post_levy_total += om_amount

        commission_rate = Decimal(str(product.default_commission_rate / 100))
        commission_amount = (net_premium * commission_rate).quantize(Decimal("0.01"))

        return MotorFinancialBreakdown(
            type="motor",
            net_premium=net_premium,
            taxes=levies,
            commission_amount=commission_amount,
            total_amount=net_premium + total_levies + post_levy_total,
            benefits=benefits,
            basic_rate=basic_rate,
            is_high_end=is_high_end,
        )


class GenericRatingStrategy(RatingStrategy):
    def calculate(
        self, product: Product, risk_details: dict[str, Any]
    ) -> MotorFinancialBreakdown:
        from app.models import PricingStrategy

        vehicle = risk_details.get("vehicle") or risk_details or {}
        value = RatingStrategy.parse_decimal(vehicle.get("sum_insured", 0))

        if product.pricing_strategy == PricingStrategy.MANUAL:
            # For manual, we can take it from risk_details if provided,
            # or use sum_insured as a fallback for some tests
            basic_premium = RatingStrategy.parse_decimal(
                risk_details.get("manual_premium") or vehicle.get("sum_insured", 0)
            )
        else:
            rate = Decimal(str(product.pricing_rules.get("rate", 0))) / Decimal("100")
            basic_premium = (value * rate).quantize(Decimal("0.01"))

        net_premium = basic_premium

        levies = self._calculate_standard_levies(net_premium)
        total_levies = sum(levies.values())

        comm_rate = Decimal(str(product.default_commission_rate)) / Decimal("100")
        commission = (net_premium * comm_rate).quantize(Decimal("0.01"))

        from app.schemas import BaseFinancialBreakdown

        return BaseFinancialBreakdown(
            type="base",
            net_premium=net_premium,
            taxes=levies,
            total_amount=net_premium + total_levies,
            commission_amount=commission,
        )


class RatingService:
    @classmethod
    def calculate_breakdown(cls, product: Product, clean_risk: dict[str, Any]) -> Any:
        if "motor private" in product.class_of_insurance.lower():
            return MotorPrivateRatingStrategy().calculate(product, clean_risk)
        return GenericRatingStrategy().calculate(product, clean_risk)
