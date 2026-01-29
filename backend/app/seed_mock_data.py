import logging
from datetime import date, timedelta

from sqlmodel import Session, select

from app.core.db import engine
from app.models import Client, Insurer, Policy, Product, RiskItem, RiskNote
from app.models.insurance.catalog import PricingStrategy

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
                pricing_strategy=PricingStrategy.PERCENTAGE,
                pricing_rules={"rate": 4.5, "min_premium": 5000},
                form_schema=[
                    {
                        "key": "registration_no",
                        "label": "Registration No",
                        "type": "text",
                    },
                    {"key": "chassis_no", "label": "Chassis No", "type": "text"},
                    {"key": "make", "label": "Make", "type": "text"},
                    {"key": "model", "label": "Model", "type": "text"},
                    {"key": "sum_insured", "label": "Sum Insured", "type": "number"},
                ],
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
                postal_address="P.O. Box 1234, Westlands, Nairobi",
                email="john@example.com",
                contacts=[
                    {
                        "name": "Jane Doe",
                        "role": "Spouse",
                        "phone": "0722000000",
                        "email": "jane@example.com",
                    }
                ],
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
        # Check if any risk item exists for this policy since identifier is gone
        item = session.exec(
            select(RiskItem).where(RiskItem.policy_id == policy.id)
        ).first()
        if not item:
            item = RiskItem(
                policy_id=policy.id,
                version_number=1,
                valid_from=date.today(),
                is_active=True,
                description="KCA 123B - Toyota Harrier",
                cover_description="Comprehensive",
                total_premium=100340.0,
                premium_breakdown={
                    "basic": 100000.0,
                    "levies": {
                        "trainingLevy": 200.0,
                        "phcf": 100.0,
                        "stampDuty": 40.0,
                    },
                    "total": 100340.0,
                },
                risk_details={
                    "make": "Toyota",
                    "model": "Harrier",
                    "chassis_no": "JMZ...",
                    "registration_no": "KCA 123B",
                    "sum_insured": 2500000.0,
                },
            )
            session.add(item)
            session.commit()
            session.refresh(item)

        # 5. CREATE RISK NOTE (The Financials)
        # Check if any risk note exists for this policy
        rn = session.exec(
            select(RiskNote).where(RiskNote.policy_id == policy.id)
        ).first()
        if not rn:
            rn = RiskNote(
                policy_id=policy.id,
                transaction_type="New Business",
                start_date=date.today(),
                end_date=date.today() + timedelta(days=365),
                net_premium=100000.0,
                taxes={
                    "trainingLevy": 200.0,
                    "phcf": 100.0,
                    "stampDuty": 40.0,
                },
                commission_amount=12500.0,
                total_amount=100340.0,
                payment_status="Unpaid",
                items_snapshot={
                    "items": [
                        {
                            "description": item.description,
                            "cover": item.cover_description,
                            "premium": item.total_premium,
                            "details": item.risk_details,
                        }
                    ]
                },
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
