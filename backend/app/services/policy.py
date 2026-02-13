import uuid
from datetime import date
from typing import Any
from sqlmodel import Session
from fastapi import HTTPException

from app import crud
from app.models import (
    Policy,
    PolicyCreate,
    RiskNote, 
    RiskNoteCreate, 
    InvoiceCreate, 
    InvoiceLineItemCreate,
    InvoiceStatus,
    RiskNoteStatus,
    Product
)
from app.schemas.insurance import MotorPrivateRiskDetails

class PolicyService:
    @staticmethod
    def create_policy(*, session: Session, policy_in: PolicyCreate) -> Policy:
        """
        Create a Policy with product-specific validation.
        """
        # 1. Product specific validation
        if policy_in.product_id:
            product = session.get(Product, policy_in.product_id)
            if product and "motor private" in product.class_of_insurance.lower():
                try:
                    # Validate risk_details against motor schema
                    MotorPrivateRiskDetails(**policy_in.risk_details)
                except Exception as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid risk details for Motor Private: {str(e)}"
                    )
        
        return crud.create_policy(session=session, policy_in=policy_in)

    @staticmethod
    def create_risk_note_with_invoice(
        *, session: Session, risk_note_in: RiskNoteCreate, created_by_id: uuid.UUID | None = None
    ) -> RiskNote:
        """
        Create a Risk Note and automatically generate its Invoice.
        This encapsulates the atomic business logic of moving from a Policy/Cover to a Financial demand.
        """
        # 1. Create the Risk Note
        if created_by_id:
            risk_note_in.created_by_id = created_by_id
            
        risk_note = crud.create_risk_note(session=session, risk_note_in=risk_note_in)
        
        # Only create invoice if it's not a Draft
        if risk_note.status != RiskNoteStatus.DRAFT:
            # 2. Create the Invoice
            policy = crud.get_policy(session=session, id=risk_note.policy_id)
            policy_num = policy.policy_number if policy else "Unknown"
            
            invoice_in = InvoiceCreate(
                invoice_number=f"INV-{uuid.uuid4().hex[:8].upper()}",
                client_id=policy.client_id if policy else risk_note_in.policy_id, # Fallback
                date_issued=date.today(),
                total_amount=risk_note.total_amount,
                balance_due=risk_note.total_amount,
                status=InvoiceStatus.UNPAID
            )
            invoice = crud.create_invoice(session=session, invoice_in=invoice_in)
            
            # 3. Create Line Item
            line_item_in = InvoiceLineItemCreate(
                invoice_id=invoice.id,
                risk_note_id=risk_note.id,
                amount=risk_note.total_amount,
                description=f"{risk_note.transaction_type} - {policy_num}"
            )
            crud.create_invoice_line_item(session=session, line_item_in=line_item_in)
            
            # 4. Link Invoice Number back to Risk Note
            risk_note.invoice_number = invoice.invoice_number
            session.add(risk_note)
            session.commit()
            session.refresh(risk_note)
            
        return risk_note

policy_service = PolicyService()
