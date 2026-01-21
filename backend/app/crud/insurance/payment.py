import uuid

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


def get_payments(session: Session, *, skip: int = 0, limit: int = 100) -> list[Payment]:
    statement = select(Payment).offset(skip).limit(limit)
    return list(session.exec(statement).all())


def count_payments(session: Session) -> int:
    from sqlmodel import func

    statement = select(func.count()).select_from(Payment)
    return session.exec(statement).one()


def delete_payment(session: Session, *, db_payment: Payment) -> None:
    session.delete(db_payment)
    session.commit()


def get_payment_allocations(
    session: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    payment_id: uuid.UUID | None = None,
    risk_note_id: uuid.UUID | None = None,
) -> list[PaymentAllocation]:
    statement = select(PaymentAllocation)
    if payment_id:
        statement = statement.where(PaymentAllocation.payment_id == payment_id)
    if risk_note_id:
        statement = statement.where(PaymentAllocation.risk_note_id == risk_note_id)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def count_payment_allocations(
    session: Session,
    *,
    payment_id: uuid.UUID | None = None,
    risk_note_id: uuid.UUID | None = None,
) -> int:
    from sqlmodel import func

    statement = select(PaymentAllocation)
    if payment_id:
        statement = statement.where(PaymentAllocation.payment_id == payment_id)
    if risk_note_id:
        statement = statement.where(PaymentAllocation.risk_note_id == risk_note_id)
    count_statement = select(func.count()).select_from(statement.subquery())
    return session.exec(count_statement).one()


def delete_payment_allocation(
    session: Session, *, db_payment_allocation: PaymentAllocation
) -> None:
    session.delete(db_payment_allocation)
    session.commit()
