import logging
import uuid
from datetime import date
from decimal import Decimal
from typing import Any

from fastapi import HTTPException
from sqlmodel import Session

from app import crud
from app.models import (
    Policy,
    PolicyCreate,
    Product,
    RiskNote,
    RiskNoteCreate,
    RiskNoteStatus,
    TransactionType,
)
from app.services.product import product_service
from app.services.rating import RatingService

logger = logging.getLogger(__name__)


def generate_risk_note_number() -> str:
    return f"RN-{uuid.uuid4().hex[:12].upper()}"


class PolicyService:
    @staticmethod
    def to_numeric_dict(data: Any) -> Any:
        """Recursively convert Decimals to strings for JSON serialization."""
        if isinstance(data, dict):
            return {k: PolicyService.to_numeric_dict(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [PolicyService.to_numeric_dict(v) for v in data]
        elif isinstance(data, Decimal):
            return str(data)
        return data

    @staticmethod
    def create_policy(
        *,
        session: Session,
        policy_in: PolicyCreate,
        cover_snapshot: dict[str, Any],
        coverage_start: date,
        coverage_end: date,
        current_user_id: uuid.UUID | None = None,
    ) -> Policy:
        """
        Create a Policy with an initial Risk Note (New Business).
        """
        product = session.get(Product, policy_in.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        try:
            validated_risk = product_service.validate_risk_details(
                product, cover_snapshot
            )
            breakdown = RatingService.calculate_breakdown(product, validated_risk)
        except Exception as e:
            logger.exception("Validation or Rating failure")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid risk details for {product.class_of_insurance}: {str(e)}",
            )

        policy = crud.create_policy(session=session, policy_in=policy_in)

        risk_note_in = RiskNoteCreate(
            policy_id=policy.id,
            transaction_type=TransactionType.NEW_BUSINESS,
            status=RiskNoteStatus.ISSUED,
            effective_date=coverage_start,
            coverage_start=coverage_start,
            coverage_end=coverage_end,
            net_premium=breakdown.net_premium,
            financial_breakdown=PolicyService.to_numeric_dict(breakdown.model_dump()),
            commission_amount=breakdown.commission_amount,
            total_amount=breakdown.total_amount,
            cover_snapshot=PolicyService.to_numeric_dict(validated_risk),
            created_by_id=current_user_id,
        )

        PolicyService.create_risk_note(session=session, risk_note_in=risk_note_in)

        return policy

    @staticmethod
    def create_risk_note(
        *,
        session: Session,
        risk_note_in: RiskNoteCreate,
        created_by_id: uuid.UUID | None = None,
    ) -> RiskNote:
        if created_by_id:
            risk_note_in.created_by_id = created_by_id

        if not risk_note_in.risk_note_number:
            risk_note_in.risk_note_number = generate_risk_note_number()

        risk_note = crud.create_risk_note(session=session, risk_note_in=risk_note_in)

        return risk_note


policy_service = PolicyService()
