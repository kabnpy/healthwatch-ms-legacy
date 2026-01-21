import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.crud.insurance.payment import (
    create_payment as crud_create_payment,
)
from app.crud.insurance.payment import (
    create_payment_allocation as crud_create_payment_allocation,
)
from app.crud.insurance.payment import (
    get_payment_by_receipt_number,
)
from app.crud.insurance.payment import (
    update_payment as crud_update_payment,
)
from app.models import (
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
    count_statement = select(func.count()).select_from(Payment)
    count = session.exec(count_statement).one()
    statement = select(Payment).offset(skip).limit(limit)
    payments = session.exec(statement).all()
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
