import uuid
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.models.insurance.financial import (
    Invoice,
    InvoiceCreate,
    InvoiceUpdate,
    Receipt,
    ReceiptCreate,
    ReceiptAllocation,
    ReceiptAllocationCreate,
)

# ==========================================
# Invoice CRUD
# ==========================================

def create_invoice(*, session: Session, invoice_in: InvoiceCreate) -> Invoice:
    db_obj = Invoice.model_validate(invoice_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def get_invoice(session: Session, *, id: uuid.UUID) -> Invoice | None:
    return session.get(Invoice, id)

def get_invoices(session: Session, *, skip: int = 0, limit: int = 100, client_id: uuid.UUID | None = None) -> list[Invoice]:
    statement = select(Invoice)
    if client_id:
        statement = statement.where(Invoice.client_id == client_id)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())

def update_invoice(*, session: Session, db_invoice: Invoice, invoice_in: InvoiceUpdate) -> Invoice:
    update_data = invoice_in.model_dump(exclude_unset=True)
    db_invoice.sqlmodel_update(update_data)
    session.add(db_invoice)
    session.commit()
    session.refresh(db_invoice)
    return db_invoice

# ==========================================
# Receipt CRUD
# ==========================================

def create_receipt(*, session: Session, receipt_in: ReceiptCreate) -> Receipt:
    db_obj = Receipt.model_validate(receipt_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def get_receipt(session: Session, *, id: uuid.UUID) -> Receipt | None:
    statement = select(Receipt).where(Receipt.id == id).options(selectinload(Receipt.allocations))
    return session.exec(statement).first()

def get_receipts(session: Session, *, skip: int = 0, limit: int = 100, client_id: uuid.UUID | None = None) -> list[Receipt]:
    statement = select(Receipt).options(selectinload(Receipt.allocations))
    if client_id:
        statement = statement.where(Receipt.client_id == client_id)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())

# ==========================================
# Allocation CRUD
# ==========================================

def create_receipt_allocation(*, session: Session, allocation_in: ReceiptAllocationCreate) -> ReceiptAllocation:
    db_obj = ReceiptAllocation.model_validate(allocation_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
