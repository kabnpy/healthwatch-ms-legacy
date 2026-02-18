from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any

from app.models import Product
from app.schemas import (
    BaseFinancialBreakdown,
    BenefitLineItem,
    MotorFinancialBreakdown,
)


class RatingStrategy(ABC):
    @abstractmethod
    def calculate(
        self, product: Product, risk_details: dict[str, Any]
    ) -> BaseFinancialBreakdown | MotorFinancialBreakdown:
        pass


class MotorPrivateRatingStrategy(RatingStrategy):
    # Default tiers if none provided in product
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
        risk_data = risk_details.get("VEHICLE DETAILS", risk_details)
        value = Decimal(str(risk_data.get("Value Kshs.", 0)))

        # 1. Basic Premium (Tiered)
        # Use tiers from product if available, else use defaults
        product_tiers = product.pricing_rules.get("tiers")
        if product_tiers:
            # Convert to Decimal for calculation
            tiers = []
            for t in product_tiers:
                tiers.append(
                    {
                        "max": Decimal(str(t["max"]))
                        if t["max"] is not None
                        else Decimal("Infinity"),
                        "rate": Decimal(str(t["rate"]))
                        / Decimal("100"),  # Convert 5.0 to 0.05
                        "min": Decimal(str(t.get("min", 0))),
                    }
                )
        else:
            tiers = self.DEFAULT_TIERS

        tier = next((t for t in tiers if value < t["max"]), tiers[-1])
        basic_rate = tier["rate"]

        basic_premium = (value * basic_rate).quantize(Decimal("0.01"))
        basic_premium = max(tier["min"], basic_premium)

        # 2. Extensions / Benefits
        extensions = risk_details.get("EXTENSIONS", {})
        benefits = []

        net_premium = basic_premium
        is_high_end = value >= Decimal("3000000")

        # Benefits logic: High-end includes PVT and Excess Protector by default at 0 cost
        include_pvt = extensions.get("pvt")
        include_ep = extensions.get("excess_protector")

        if include_pvt:
            if is_high_end:
                benefits.append(BenefitLineItem(name="PVT", amount=Decimal("0.00")))
            else:
                pvt_amount = (value * Decimal("0.0025")).quantize(Decimal("0.01"))
                benefits.append(BenefitLineItem(name="PVT", amount=pvt_amount))
                net_premium += pvt_amount

        if include_ep:
            if is_high_end:
                benefits.append(
                    BenefitLineItem(name="Excess Protector", amount=Decimal("0.00"))
                )
            else:
                ep_amount = (value * Decimal("0.0025")).quantize(Decimal("0.01"))
                benefits.append(
                    BenefitLineItem(name="Excess Protector", amount=ep_amount)
                )
                net_premium += ep_amount

        if extensions.get("passenger_liability") or extensions.get(
            "passengerLiability"
        ):
            pl_amount = Decimal("500.00")
            benefits.append(
                BenefitLineItem(name="Passenger Liability", amount=pl_amount)
            )
            net_premium += pl_amount

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
            benefits=benefits,
            basic_rate=basic_rate,
            is_high_end=is_high_end,
        )

    def _calculate_standard_levies(self, net_premium: Decimal) -> dict[str, Decimal]:
        training_levy = (net_premium * Decimal("0.002")).quantize(Decimal("0.01"))
        phcf = (net_premium * Decimal("0.0025")).quantize(Decimal("0.01"))
        stamp_duty = Decimal("40.00")

        return {"training_levy": training_levy, "phcf": phcf, "stamp_duty": stamp_duty}


class RatingService:
    _strategies: dict[str, RatingStrategy] = {
        "motor private": MotorPrivateRatingStrategy()
    }

    @classmethod
    def calculate_levies(cls, net_premium: Decimal) -> dict[str, Decimal]:
        # Uses the standard Kenyan levies logic
        strategy = MotorPrivateRatingStrategy()  # Both currently use same levies
        return strategy._calculate_standard_levies(net_premium)

    @classmethod
    def calculate_breakdown(
        cls, product: Product, risk_details: dict[str, Any]
    ) -> BaseFinancialBreakdown | MotorFinancialBreakdown:
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
    def _calculate_generic(
        cls, product: Product, risk_details: dict[str, Any]
    ) -> BaseFinancialBreakdown:
        # Placeholder for other products
        net_premium = Decimal("0.00")
        stamp_duty = Decimal("40.00")

        return BaseFinancialBreakdown(
            type="base",
            net_premium=net_premium,
            taxes={"stamp_duty": stamp_duty},
            commission_amount=Decimal("0.00"),
            total_amount=net_premium + stamp_duty,
        )
