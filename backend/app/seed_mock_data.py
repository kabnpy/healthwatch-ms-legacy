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
        old_mutual = session.exec(
            select(Insurer).where(Insurer.name == "Old Mutual General Insurance Kenya Ltd.")
        ).first()
        if not old_mutual:
            old_mutual = Insurer(name="Old Mutual General Insurance Kenya Ltd.", email="info@oldmutual.co.ke")
            session.add(old_mutual)
            session.commit()
            session.refresh(old_mutual)

        # PRODUCT: PERSONAL ACCIDENT
        pa_product = session.exec(select(Product).where(Product.name == "Maxpac Personal Accident")).first()
        if not pa_product:
            pa_product = Product(
                insurer_id=old_mutual.id,
                name="Maxpac Personal Accident",
                class_of_insurance="Personal Accident",
                product_details=[
                    # Inputs
                    {"key": "occupation", "label": "Occupation", "type": "text", "field_type": "input", "section": "OCCUPATION", "pricing_type": "none"},
                    
                    # Static Benefits (Precalculated/Flat)
                    {"key": "acc_death", "label": "Accidental Death", "type": "static", "field_type": "static", "section": "BENEFITS", "value": "Kshs. 500,000/-", "pricing_type": "none"},
                    {"key": "perm_total_disability", "label": "Permanent Total Disablement", "type": "static", "field_type": "static", "section": "BENEFITS", "value": "Kshs. 500,000/-", "pricing_type": "none"},
                    
                    # The Premium itself
                    {"key": "base_premium", "label": "Standard PA Premium", "type": "number", "field_type": "static", "section": "FINANCIALS", "value": 1725.0, "pricing_type": "fixed", "pricing_value": 1725.0, "show_in_risknote": False},
                ],
            )
            session.add(pa_product)

        # PRODUCT: MOTOR PRIVATE
        motor_product = session.exec(select(Product).where(Product.name == "Motor Private - Comprehensive")).first()
        if not motor_product:
            motor_product = Product(
                insurer_id=old_mutual.id,
                name="Motor Private - Comprehensive",
                class_of_insurance="Motor Private",
                product_details=[
                    # Inputs
                    {"key": "reg_no", "label": "Reg. No", "type": "text", "field_type": "input", "section": "VEHICLE DETAILS", "pricing_type": "none"},
                    {"key": "make", "label": "Make", "type": "text", "field_type": "input", "section": "VEHICLE DETAILS", "pricing_type": "none"},
                    {"key": "year", "label": "Year", "type": "number", "field_type": "input", "section": "VEHICLE DETAILS", "pricing_type": "none"},
                    {"key": "value", "label": "Value Kshs.", "type": "number", "field_type": "input", "section": "VEHICLE DETAILS", "pricing_type": "percentage", "pricing_value": 3.25},
                    
                    # Static Benefits
                    {"key": "tp_persons", "label": "Third Party Persons", "type": "static", "field_type": "static", "section": "HIGH-END BENEFITS & LIMITS", "value": "Kshs. 10,000,000.00", "pricing_type": "none"},
                ],
            )
            session.add(motor_product)

        # PRODUCT: DOMESTIC PACKAGE
        domestic_product = session.exec(select(Product).where(Product.name == "Domestic Package - HomeShield")).first()
        if not domestic_product:
            domestic_product = Product(
                insurer_id=old_mutual.id,
                name="Domestic Package - HomeShield",
                class_of_insurance="Domestic Package",
                product_details=[
                    # Inputs
                    {"key": "location", "label": "Location", "type": "text", "field_type": "input", "section": "LOCATION", "pricing_type": "none"},
                    {"key": "value", "label": "Value Kshs.", "type": "number", "field_type": "input", "section": "LOCATION", "pricing_type": "percentage", "pricing_value": 1.5},
                ],
            )
            session.add(domestic_product)

        session.commit()
        logger.info("✅ Catalog Seeded with Unified product_details")

        # 2. CREATE CLIENT (Agnes Njoki Mwangi)
        client = session.exec(
            select(Client).where(Client.kra_pin == "A001158997L")
        ).first()
        if not client:
            client = Client(
                name="Agnes Njoki Mwangi",
                kra_pin="A001158997L",
                phone="0733980566",
                postal_address="P.O. Box 11908 - 00100",
                city="Nairobi",
                email="agnes@example.com",
            )
            session.add(client)
            session.commit()
            session.refresh(client)

        # 3. CREATE MOTOR POLICY
        policy = session.exec(
            select(Policy).where(Policy.policy_number == "010/070/1/012473/2017")
        ).first()
        if not policy:
            policy = Policy(
                policy_number="010/070/1/012473/2017",
                client_id=client.id,
                product_id=motor_product.id,
                status="Active",
            )
            session.add(policy)
            session.commit()
            session.refresh(policy)

        # 4. CREATE MOTOR RISK ITEM
        item = session.exec(
            select(RiskItem).where(RiskItem.policy_id == policy.id)
        ).first()
        if not item:
            item = RiskItem(
                policy_id=policy.id,
                description="KCM 780L - Toyota Landcruiser Prado",
                cover_description="Comprehensive",
                total_premium=153438.0,
                premium_breakdown={
                    "basic": 152750.0,
                    "levies": {"trainingLevy": 306.0, "phcf": 382.0},
                },
                risk_details={
                    "reg_no": "KCM 780L",
                    "make": "Toyota Landcruiser Prado",
                    "year": 2016,
                    "value": 4700000.0,
                },
            )
            session.add(item)
            session.commit()
            session.refresh(item)

        # 5. CREATE MOTOR RISK NOTE
        rn = session.exec(
            select(RiskNote).where(RiskNote.policy_id == policy.id)
        ).first()
        if not rn:
            rn = RiskNote(
                policy_id=policy.id,
                transaction_type="New Business",
                invoice_number="HW-MOT-001",
                start_date=date(2025, 8, 2),
                end_date=date(2026, 8, 1),
                net_premium=152750.0,
                taxes={"trainingLevy": 306.0, "phcf": 382.0},
                commission_amount=15275.0,
                total_amount=153438.0,
                status="Active",
                items_snapshot={
                    "items": [
                        {
                            "name": motor_product.name,
                            "description": item.description,
                            "cover": item.cover_description,
                            "premium": item.total_premium,
                            "details": item.risk_details,
                        }
                    ]
                },
                special_clauses=[],
            )
            session.add(rn)
            session.commit()

        logger.info("✅ Mock Data Seeded Successfully")


if __name__ == "__main__":
    create_mock_data()
