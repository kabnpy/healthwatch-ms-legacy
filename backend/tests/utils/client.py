from sqlmodel import Session

from app import crud
from app.models import Client, ClientCreate
from tests.utils.utils import random_email, random_lower_string


def create_random_client(db: Session) -> Client:
    name = random_lower_string()
    kra_pin = random_lower_string()
    email = random_email()
    phone = random_lower_string()
    client_in = ClientCreate(name=name, kra_pin=kra_pin, email=email, phone=phone)
    return crud.create_client(session=db, client_in=client_in)
