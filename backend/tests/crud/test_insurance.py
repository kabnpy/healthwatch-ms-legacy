from sqlmodel import Session

from app import crud
from app.models import (
    InsurerCreate,
    ProductCreate,
    ClientCreate,
    PolicyCreate,
    RiskNoteCreate,
    ReceiptCreate,
    ReceiptAllocationCreate,
)
from tests.utils.utils import random_lower_string, random_email
import uuid
from datetime import date


def test_create_insurer(db: Session) -> None:
    name = random_lower_string()
    insurer_in = InsurerCreate(name=name, email=random_email())
    insurer = crud.create_insurer(session=db, insurer_in=insurer_in)
    assert insurer.name == name
    assert insurer.email is not None


def test_create_product(db: Session) -> None:
    insurer_in = InsurerCreate(name=random_lower_string(), email=random_email())
    insurer = crud.create_insurer(session=db, insurer_in=insurer_in)
    
    product_in = ProductCreate(
        insurer_id=insurer.id,
        name=random_lower_string(),
        class_of_insurance="Motor Private",
    )
    product = crud.create_product(session=db, product_in=product_in)
    assert product.name == product_in.name
    assert product.insurer_id == insurer.id


def test_create_client(db: Session) -> None:
    client_in = ClientCreate(
        name=random_lower_string(),
        kra_pin=random_lower_string(),
        email=random_email(),
        phone=random_lower_string(),
    )
    client = crud.create_client(session=db, client_in=client_in)
    assert client.name == client_in.name
    assert client.email == client_in.email


def test_create_policy(db: Session) -> None:
    client_in = ClientCreate(
        name=random_lower_string(),
        kra_pin=random_lower_string(),
        email=random_email(),
        phone=random_lower_string(),
    )
    client = crud.create_client(session=db, client_in=client_in)
    
    policy_in = PolicyCreate(
        policy_number=random_lower_string(),
        client_id=client.id,
    )
    policy = crud.create_policy(session=db, policy_in=policy_in)
    assert policy.policy_number == policy_in.policy_number
    assert policy.client_id == client.id


def test_create_risk_note(db: Session) -> None:
    client_in = ClientCreate(
        name=random_lower_string(),
        kra_pin=random_lower_string(),
        email=random_email(),
        phone=random_lower_string(),
    )
    client = crud.create_client(session=db, client_in=client_in)
    
    policy_in = PolicyCreate(
        policy_number=random_lower_string(),
        client_id=client.id,
    )
    policy = crud.create_policy(session=db, policy_in=policy_in)
    
    risk_note_in = RiskNoteCreate(
        risk_note_number=random_lower_string(),
        policy_id=policy.id,
        transaction_type="New Business",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        premium_breakdown={"basic": 1000.0, "total": 1100.0},
        commission_amount=100.0,
    )
    risk_note = crud.create_risk_note(session=db, risk_note_in=risk_note_in)
    assert risk_note.risk_note_number == risk_note_in.risk_note_number
    assert risk_note.policy_id == policy.id


def test_create_receipt(db: Session) -> None:
    client_in = ClientCreate(
        name=random_lower_string(),
        kra_pin=random_lower_string(),
        email=random_email(),
        phone=random_lower_string(),
    )
    client = crud.create_client(session=db, client_in=client_in)

    receipt_in = ReceiptCreate(
        receipt_number=random_lower_string(),
        client_id=client.id,
        date_received=date(2024, 1, 15),
        amount=1100.0,
        mode="Cash",
        reference=random_lower_string(),
    )
    receipt = crud.create_receipt(session=db, receipt_in=receipt_in)
    assert receipt.receipt_number == receipt_in.receipt_number
    assert receipt.amount == receipt_in.amount


def test_create_receipt_allocation(db: Session) -> None:
    client_in = ClientCreate(
        name=random_lower_string(),
        kra_pin=random_lower_string(),
        email=random_email(),
        phone=random_lower_string(),
    )
    client = crud.create_client(session=db, client_in=client_in)
    
    policy_in = PolicyCreate(
        policy_number=random_lower_string(),
        client_id=client.id,
    )
    policy = crud.create_policy(session=db, policy_in=policy_in)
    
    risk_note_in = RiskNoteCreate(
        risk_note_number=random_lower_string(),
        policy_id=policy.id,
        transaction_type="New Business",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        premium_breakdown={"basic": 1000.0, "total": 1100.0},
        commission_amount=100.0,
    )
    risk_note = crud.create_risk_note(session=db, risk_note_in=risk_note_in)
    
    receipt_in = ReceiptCreate(
        receipt_number=random_lower_string(),
        client_id=client.id,
        date_received=date(2024, 1, 15),
        amount=1100.0,
        mode="Cash",
        reference=random_lower_string(),
    )
    receipt = crud.create_receipt(session=db, receipt_in=receipt_in)
    
    # We need an invoice for the allocation
    # The risk_note creation already creates an invoice in crud.create_risk_note
    from app.models.insurance.financial import Invoice
    from sqlmodel import select
    invoice = db.exec(select(Invoice).where(Invoice.client_id == client.id)).first()
    assert invoice is not None

    allocation_in = ReceiptAllocationCreate(
        receipt_id=receipt.id,
        invoice_id=invoice.id,
        risk_note_id=risk_note.id,
        amount_allocated=1100.0,
    )
    allocation = crud.create_receipt_allocation(session=db, allocation_in=allocation_in)
    assert allocation.receipt_id == receipt.id
    assert allocation.risk_note_id == risk_note.id
