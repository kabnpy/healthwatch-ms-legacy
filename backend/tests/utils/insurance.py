import uuid
from datetime import date
from sqlmodel import Session

from app import crud
from app.models import (
    Insurer, InsurerCreate,
    Product, ProductCreate,
    Policy, PolicyCreate,
    RiskNote, RiskNoteCreate,
    Payment, PaymentCreate,
    Claim, ClaimCreate
)
from tests.utils.utils import random_email, random_lower_string
from tests.utils.client import create_random_client

def create_random_insurer(db: Session) -> Insurer:
    name = random_lower_string()
    email = random_email()
    insurer_in = InsurerCreate(name=name, email=email)
    return crud.create_insurer(session=db, insurer_in=insurer_in)

def create_random_product(db: Session, insurer_id: uuid.UUID | None = None) -> Product:
    if not insurer_id:
        insurer = create_random_insurer(db)
        insurer_id = insurer.id
    name = random_lower_string()
    product_in = ProductCreate(
        insurer_id=insurer_id,
        name=name,
        class_of_insurance="Motor Private"
    )
    return crud.create_product(session=db, product_in=product_in)

def create_random_policy(db: Session, client_id: uuid.UUID | None = None, product_id: uuid.UUID | None = None) -> Policy:
    if not client_id:
        client = create_random_client(db)
        client_id = client.id
    if not product_id:
        product = create_random_product(db)
        product_id = product.id
    
    policy_number = random_lower_string()
    policy_in = PolicyCreate(
        policy_number=policy_number,
        client_id=client_id,
        product_id=product_id
    )
    return crud.create_policy(session=db, policy_in=policy_in)

def create_random_payment(db: Session) -> Payment:
    receipt_number = random_lower_string()
    payment_in = PaymentCreate(
        receipt_number=receipt_number,
        date_received=date.today(),
        amount=1000.0,
        mode="Cash",
        reference=random_lower_string()
    )
    return crud.create_payment(session=db, payment_in=payment_in)

def create_random_claim(db: Session, policy_id: uuid.UUID | None = None) -> Claim:
    if not policy_id:
        policy = create_random_policy(db)
        policy_id = policy.id
    
    claim_number = random_lower_string()
    claim_in = ClaimCreate(
        claim_number=claim_number,
        policy_id=policy_id,
        date_of_loss=date.today(),
        description="Fender bender"
    )
    return crud.create_claim(session=db, claim_in=claim_in)
