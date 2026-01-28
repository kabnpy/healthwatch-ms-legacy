import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUser, SessionDep
from app.crud.insurance.payment import (
    count_payments,
    get_payment_by_receipt_number,
    get_payments,
)
from app.crud.insurance.payment import (
    create_payment as crud_create_payment,
)
from app.crud.insurance.payment import (
    create_payment_allocation as crud_create_payment_allocation,
)
from app.crud.insurance.payment import (
    delete_payment as crud_delete_payment,
)
from app.crud.insurance.payment import (
    update_payment as crud_update_payment,
)
from app.models import (
    Message,
    Payment,
    PaymentAllocationCreate,
    PaymentAllocationPublic,
    PaymentCreate,
    PaymentPublic,
    PaymentsPublic,
    PaymentUpdate,
)

router = APIRouter()


@router.get("/", response_model=PaymentsPublic)
def read_payments(
    session: SessionDep, _current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve payments.
    """
    count = count_payments(session=session)
    payments = get_payments(session=session, skip=skip, limit=limit)
    return PaymentsPublic(data=payments, count=count)


@router.get("/{id}", response_model=PaymentPublic)
def read_payment(session: SessionDep, _current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get payment by ID.
    """
    payment = session.get(Payment, id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.post("/", response_model=PaymentPublic)
def create_payment(
    *, session: SessionDep, _current_user: CurrentUser, payment_in: PaymentCreate
) -> Any:
    """
    Create new payment (Receipt).
    """
    existing_payment = get_payment_by_receipt_number(
        session=session, receipt_number=payment_in.receipt_number
    )
    if existing_payment:
        raise HTTPException(
            status_code=400,
            detail="The payment with this receipt number already exists.",
        )

    payment = crud_create_payment(session=session, payment_in=payment_in)
    return payment


@router.put("/{id}", response_model=PaymentPublic)
def update_payment(
    *,
    session: SessionDep,
    _current_user: CurrentUser,
    id: uuid.UUID,
    payment_in: PaymentUpdate,
) -> Any:
    """
    Update a payment.
    """
    payment = session.get(Payment, id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    payment = crud_update_payment(
        session=session, db_payment=payment, payment_in=payment_in
    )
    return payment


@router.delete("/{id}", response_model=Message)
def delete_payment(
    session: SessionDep, _current_user: CurrentUser, id: uuid.UUID
) -> Any:
    """
    Delete a payment.
    """
    payment = session.get(Payment, id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    crud_delete_payment(session=session, db_payment=payment)
    return Message(message="Payment deleted successfully")


@router.post("/{id}/allocations", response_model=PaymentAllocationPublic)
def create_payment_allocation(
    *,
    session: SessionDep,
    _current_user: CurrentUser,
    id: uuid.UUID,
    allocation_in: PaymentAllocationCreate,
) -> Any:
    """
    Allocate payment to a risk note.
    """
    payment = session.get(Payment, id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if allocation_in.payment_id != id:
        raise HTTPException(status_code=400, detail="Payment ID mismatch")

    allocation = crud_create_payment_allocation(
        session=session, payment_allocation_in=allocation_in
    )
    return allocation
