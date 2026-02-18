import uuid
from datetime import date
from decimal import Decimal
from typing import Any

from fastapi import HTTPException
from sqlmodel import Session

from app import crud
from app.services.rating import RatingService
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

        # 1. Validate and price
        try:
            validated_risk = product.validate_risk_details(risk_details)
            breakdown = RatingService.calculate_breakdown(product, risk_details)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid risk details for {product.class_of_insurance}: {str(e)}",
            )

        # 2. Create Policy (container)
        policy = crud.create_policy(session=session, policy_in=policy_in)

        # 3. Create initial Risk Note
        risk_note_in = RiskNoteCreate(
            policy_id=policy.id,
            transaction_type=TransactionType.NEW_BUSINESS,
            status=RiskNoteStatus.ISSUED,
            effective_date=coverage_start,
            coverage_start=coverage_start,
            coverage_end=coverage_end,
            policy_snapshot={
                "policy_number": policy.policy_number,
                "risk_details": validated_risk,
                "product": product.model_dump(mode="json"),
            },
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
            full_breakdown = RatingService.calculate_breakdown(product, updated_risk_details)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid risk details for {product.class_of_insurance}: {str(e)}",
            )

        # 2. Calculate delta (pro-rata logic could be added here, for now it's just delta of full term)
        delta_premium = full_breakdown.net_premium - current_rn.net_premium

        # 3. Create NEW risk note
        # We store the full authoritative breakdown for the new state
        risk_note_in = RiskNoteCreate(
            policy_id=policy.id,
            transaction_type=TransactionType.ENDORSEMENT,
            previous_risk_note_id=current_rn.id,
            status=RiskNoteStatus.ISSUED,
            effective_date=date.today(),
            coverage_start=current_rn.coverage_start,
            coverage_end=current_rn.coverage_end,
            policy_snapshot={
                "policy_number": policy.policy_number,
                "risk_details": validated_risk,
                "product": product.model_dump(mode="json"),
                "changes": {
                    "description": change_description,
                    "from": current_rn.policy_snapshot.get("risk_details"),
                    "to": validated_risk,
                },
            },
            net_premium=delta_premium,
            financial_breakdown=full_breakdown.model_dump(mode="json"),
            commission_amount=full_breakdown.commission_amount - current_rn.commission_amount,
            total_amount=full_breakdown.total_amount - current_rn.total_amount,
            special_clauses=[change_description],
            created_by_id=current_user_id,
        )

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
