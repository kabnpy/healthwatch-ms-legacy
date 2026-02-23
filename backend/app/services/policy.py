import logging
import uuid
from datetime import date
from typing import Any

from fastapi import HTTPException
from sqlmodel import Session

from app import crud
from app.models import (
    InvoiceCreate,
    InvoiceLineItemCreate,
    InvoiceStatus,
    Policy,
    PolicyCreate,
    Product,
    RiskNote,
    RiskNoteCreate,
    RiskNoteStatus,
    TransactionType,
)
from app.services.rating import RatingService

logger = logging.getLogger(__name__)


def generate_risk_note_number() -> str:
    return f"RN-{uuid.uuid4().hex[:8].upper()}"


class PolicyService:
    @staticmethod
    def create_policy(
        *,
        session: Session,
        policy_in: PolicyCreate,
        risk_details: dict[str, Any],
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

        logger.info(f"Creating policy for product: {product.name} ({product.class_of_insurance})")
        logger.debug(f"Input risk_details: {risk_details}")

        # 1. Validate and price
        try:
            validated_risk = product.validate_risk_details(risk_details)
            logger.debug(f"Validated risk details: {validated_risk}")

            # Ensure extensions are available for rating
            rating_details = validated_risk.copy()
            if "EXTENSIONS" not in rating_details and "EXTENSIONS" in risk_details:
                rating_details["EXTENSIONS"] = risk_details["EXTENSIONS"]
                
            breakdown = RatingService.calculate_breakdown(product, rating_details)
            logger.info(f"Rating breakdown: {breakdown.model_dump()}")
        except Exception as e:
            logger.exception("Validation or Rating failure")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid risk details for {product.class_of_insurance}: {str(e)}",
            )

        # 2. Create Policy (container)
        policy_in.risk_details = rating_details
        policy = crud.create_policy(session=session, policy_in=policy_in)

        # 3. Create initial Risk Note
        risk_note_in = RiskNoteCreate(
            policy_id=policy.id,
            transaction_type=TransactionType.NEW_BUSINESS,
            status=RiskNoteStatus.ISSUED,
            effective_date=coverage_start,
            coverage_start=coverage_start,
            coverage_end=coverage_end,
            net_premium=breakdown.net_premium,
            financial_breakdown=breakdown.model_dump(mode="json"),
            commission_amount=breakdown.commission_amount,
            total_amount=breakdown.total_amount,
            created_by_id=current_user_id,
        )

        PolicyService.create_risk_note_with_invoice(
            session=session, risk_note_in=risk_note_in
        )

        session.refresh(policy)
        return policy
    @staticmethod
    def create_endorsement(
        *,
        session: Session,
        policy_id: uuid.UUID,
        updated_risk_details: dict[str, Any],
        change_description: str,
        current_user_id: uuid.UUID | None = None,
    ) -> RiskNote:
        """
        Create a mid-term modification (Endorsement).
        """
        policy = session.get(Policy, policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")

        product = policy.product
        if not product:
            raise HTTPException(
                status_code=400, detail="Policy has no product assigned"
            )

        current_rn = policy.current_risk_note
        if not current_rn:
            raise HTTPException(
                status_code=400, detail="Cannot endorse policy without active risk note"
            )

        # 1. Validate and price NEW state
        try:
            validated_risk = product.validate_risk_details(updated_risk_details)
            # Ensure extensions are available for rating
            rating_details = validated_risk.copy()
            if (
                "EXTENSIONS" not in rating_details
                and "EXTENSIONS" in updated_risk_details
            ):
                rating_details["EXTENSIONS"] = updated_risk_details["EXTENSIONS"]

            full_breakdown = RatingService.calculate_breakdown(product, rating_details)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid risk details for {product.class_of_insurance}: {str(e)}",
            )

        # 2. Calculate delta
        delta_net_premium = full_breakdown.net_premium - current_rn.net_premium
        delta_total_amount = full_breakdown.total_amount - current_rn.total_amount
        delta_commission = full_breakdown.commission_amount - current_rn.commission_amount

        # 3. Calculate diff for change_log
        current_risk = policy.risk_details
        diff = {}
        for k, v in rating_details.items():
            if current_risk.get(k) != v:
                diff[k] = {"from": current_risk.get(k), "to": v}

        # 4. Structure the breakdown with both new state and delta
        financial_breakdown = {
            "new_state": full_breakdown.model_dump(mode="json"),
            "delta": {
                "net_premium": float(delta_net_premium),
                "total_amount": float(delta_total_amount),
                "commission_amount": float(delta_commission),
            }
        }

        # 5. Create NEW risk note
        risk_note_in = RiskNoteCreate(
            policy_id=policy.id,
            transaction_type=TransactionType.ENDORSEMENT,
            previous_risk_note_id=current_rn.id,
            status=RiskNoteStatus.ISSUED,
            effective_date=date.today(),
            coverage_start=current_rn.coverage_start,
            coverage_end=current_rn.coverage_end,
            change_log=diff,
            net_premium=delta_net_premium,
            financial_breakdown=financial_breakdown,
            commission_amount=delta_commission,
            total_amount=delta_total_amount,
            special_clauses=[change_description],
            created_by_id=current_user_id,
        )

        # 6. Update Policy state in-place
        policy.risk_details = rating_details
        session.add(policy)

        # Mark previous as replaced
        current_rn.status = RiskNoteStatus.REPLACED
        session.add(current_rn)

        return PolicyService.create_risk_note_with_invoice(
            session=session, risk_note_in=risk_note_in
        )

    @staticmethod
    def create_risk_note_with_invoice(
        *,
        session: Session,
        risk_note_in: RiskNoteCreate,
        created_by_id: uuid.UUID | None = None,
    ) -> RiskNote:
        """
        Create a Risk Note and automatically generate its Invoice.
        """
        if created_by_id:
            risk_note_in.created_by_id = created_by_id

        if not risk_note_in.risk_note_number:
            risk_note_in.risk_note_number = generate_risk_note_number()

        risk_note = crud.create_risk_note(session=session, risk_note_in=risk_note_in)

        # Only create invoice if it's not a Draft
        if risk_note.status != RiskNoteStatus.DRAFT:
            policy = crud.get_policy(session=session, id=risk_note.policy_id)
            if not policy:
                raise HTTPException(
                    status_code=404, detail="Policy not found for invoice generation"
                )

            policy_num = policy.policy_number
            invoice_in = InvoiceCreate(
                invoice_number=f"INV-{uuid.uuid4().hex[:8].upper()}",
                client_id=policy.client_id,
                date_issued=date.today(),
                total_amount=risk_note.total_amount,
                balance_due=risk_note.total_amount,
                status=InvoiceStatus.UNPAID,
            )
            invoice = crud.create_invoice(session=session, invoice_in=invoice_in)

            line_item_in = InvoiceLineItemCreate(
                invoice_id=invoice.id,
                risk_note_id=risk_note.id,
                amount=risk_note.total_amount,
                description=f"{risk_note.transaction_type} - {policy_num}",
            )
            crud.create_invoice_line_item(session=session, line_item_in=line_item_in)

            risk_note.invoice_number = invoice.invoice_number
            session.add(risk_note)
            session.commit()
            session.refresh(risk_note)

        return risk_note


policy_service = PolicyService()
