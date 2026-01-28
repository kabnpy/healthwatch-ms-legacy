import logging
from datetime import date, timedelta

from sqlmodel import Session, select

from app.core.db import engine
from app.models import Client, Insurer, Policy, Product, RiskItem, RiskNote

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_mock_data() -> None:
    with Session(engine) as session:
        # 1. SETUP THE CATALOG
        insurer = session.exec(
            select(Insurer).where(Insurer.name == "Jubilee Insurance")
        ).first()
        if not insurer:
            insurer = Insurer(name="Jubilee Insurance", email="claims@jubilee.com")
            session.add(insurer)
            session.commit()
            session.refresh(insurer)

        product = session.exec(
            select(Product).where(Product.name == "Motor Private - Gold")
        ).first()
        if not product:
            product = Product(
                insurer_id=insurer.id,
                name="Motor Private - Gold",
                class_of_insurance="Motor Private",
                default_benefits={
                    "towing": 50000,
                    "windscreen": 50000,
                    "excess": "2.5% of Value",
                },
                default_commission_rate=12.5,
            )
            session.add(product)
            session.commit()
            session.refresh(product)

        # 2. CREATE CLIENT
        client = session.exec(
            select(Client).where(Client.kra_pin == "A001234567Z")
        ).first()
        if not client:
            client = Client(
                name="John Doe",
                kra_pin="A001234567Z",
                phone="0712345678",
                postal_address="Westlands, Nairobi",
                email="john@example.com",
            )
            session.add(client)
            session.commit()
            session.refresh(client)

        # 3. CREATE POLICY
        policy = session.exec(
            select(Policy).where(Policy.policy_number == "P/001/2026")
        ).first()
        if not policy:
            policy = Policy(
                policy_number="P/001/2026",
                client_id=client.id,
                product_id=product.id,
                status="Active",
            )
            session.add(policy)
            session.commit()
            session.refresh(policy)

        # 4. CREATE RISK ITEM (The Car)
        item = session.exec(
            select(RiskItem).where(RiskItem.identifier == "KCA 123B")
        ).first()
        if not item:
            item = RiskItem(
                policy_id=policy.id,
                identifier="KCA 123B",
                description="Toyota Harrier",
                sum_insured=2500000.0,
                details={"make": "Toyota", "chassis": "JMZ..."},
                benefits=product.default_benefits,
            )
            session.add(item)
            session.commit()
            session.refresh(item)

        # 5. CREATE RISK NOTE (The Financials)
        rn = session.exec(
            select(RiskNote).where(RiskNote.risk_note_number == "RN/001/26")
        ).first()
        if not rn:
            rn = RiskNote(
                risk_note_number="RN/001/26",
                policy_id=policy.id,
                transaction_type="New Business",
                start_date=date.today(),
                end_date=date.today() + timedelta(days=365),
                premium_breakdown={
                    "basic": 100000.0,
                    "levies": {
                        "trainingLevy": 200.0,
                        "phcf": 100.0,
                        "stampDuty": 40.0,
                    },
                    "total": 100340.0,
                },
                benefits_snapshot=item.benefits,
                risk_item_snapshot={
                    "identifier": item.identifier,
                    "description": item.description,
                    "details": item.details,
                },
                commission_amount=12500.0,
                special_clauses=[
                    "Including Political Violence",
                    "Windscreen up to 50k",
                ],
            )
            session.add(rn)
            session.commit()

        logger.info("✅ Mock Data Seeded Successfully")


if __name__ == "__main__":
    create_mock_data()
