from decimal import Decimal
from typing import Any

from app.models import Product
from app.services.rating import RatingService


class ProductService:
    @staticmethod
    def validate_risk_details(
        product: Product, risk_details: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Validate risk details based on product type.
        """
        if "motor private" in product.class_of_insurance.lower():
            from app.schemas import MotorPrivateRiskDetails

            validated = MotorPrivateRiskDetails(**risk_details)
            return validated.model_dump(mode="python")
        return risk_details

    @staticmethod
    def calculate_premium(product: Product, risk_details: dict[str, Any]) -> Decimal:
        """
        Calculate net premium for a product given risk details.
        """
        breakdown = RatingService.calculate_breakdown(product, risk_details)
        return breakdown.net_premium


product_service = ProductService()
