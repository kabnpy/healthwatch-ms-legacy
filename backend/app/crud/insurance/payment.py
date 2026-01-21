from sqlmodel import Session, select

from app.models.insurance.payment import (
    Payment,
    PaymentAllocation,
    PaymentAllocationCreate,
    PaymentAllocationUpdate,
    PaymentCreate,
    PaymentUpdate,
)


def create_payment(*, session: Session, payment_in: PaymentCreate) -> Payment:
    db_obj = Payment.model_validate(payment_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_payment_by_receipt_number(
    session: Session, *, receipt_number: str
) -> Payment | None:
    statement = select(Payment).where(Payment.receipt_number == receipt_number)
    return session.exec(statement).first()


def update_payment(
    *, session: Session, db_payment: Payment, payment_in: PaymentUpdate
) -> Payment:
    payment_data = payment_in.model_dump(exclude_unset=True)
    db_payment.sqlmodel_update(payment_data)
    session.add(db_payment)
    session.commit()
    session.refresh(db_payment)
    return db_payment


def create_payment_allocation(
    *, session: Session, payment_allocation_in: PaymentAllocationCreate
) -> PaymentAllocation:
    db_obj = PaymentAllocation.model_validate(payment_allocation_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_payment_allocation(
    *,
    session: Session,
    db_payment_allocation: PaymentAllocation,
    payment_allocation_in: PaymentAllocationUpdate,
) -> PaymentAllocation:
    payment_allocation_data = payment_allocation_in.model_dump(exclude_unset=True)
    db_payment_allocation.sqlmodel_update(payment_allocation_data)
    session.add(db_payment_allocation)
    session.commit()
    session.refresh(db_payment_allocation)
    return db_payment_allocation
