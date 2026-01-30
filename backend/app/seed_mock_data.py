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
                form_schema=[
                    {"key": "occupation", "label": "Occupation", "type": "text"},
                    {"key": "acc_death", "label": "Accidental Death", "type": "number", "category": "BENEFITS"},
                    {"key": "perm_total_disability", "label": "Permanent Total Disablement", "type": "number", "category": "BENEFITS"},
                    {"key": "hosp_cash", "label": "Hospital Cash", "type": "number", "category": "BENEFITS"},
                    {"key": "acc_med_expenses", "label": "Accidental Medical Expenses", "type": "number", "category": "BENEFITS"},
                    {"key": "last_expense", "label": "Last Expense", "type": "number", "category": "BENEFITS"},
                ],
                default_benefits={
                    "acc_death": 500000,
                    "perm_total_disability": 500000,
                    "hosp_cash": 1000,
                    "acc_med_expenses": 70000,
                    "last_expense": 50000,
                },
                default_clauses=["24hour cover", "Worldwide limits", "Age limits 16-65 years"],
            )
            session.add(pa_product)

        # PRODUCT: MOTOR PRIVATE
        motor_product = session.exec(select(Product).where(Product.name == "Motor Private - Comprehensive")).first()
        if not motor_product:
            motor_product = Product(
                insurer_id=old_mutual.id,
                name="Motor Private - Comprehensive",
                class_of_insurance="Motor Private",
                form_schema=[
                    {"key": "reg_no", "label": "Reg. No", "type": "text", "category": "VEHICLE DETAILS"},
                    {"key": "make", "label": "Make", "type": "text", "category": "VEHICLE DETAILS"},
                    {"key": "year", "label": "Year", "type": "number", "category": "VEHICLE DETAILS"},
                    {"key": "value", "label": "Value Kshs.", "type": "number", "category": "VEHICLE DETAILS"},
                    {"key": "tp_persons", "label": "Third Party Persons", "type": "number", "category": "BENEFITS & LIMITS"},
                    {"key": "tp_property", "label": "Third Party Property", "type": "number", "category": "BENEFITS & LIMITS"},
                    {"key": "towing", "label": "Towing & Recovery", "type": "number", "category": "BENEFITS & LIMITS"},
                    {"key": "own_damage_excess", "label": "Own Damage and Partial", "type": "text", "category": "EXCESS"},
                    {"key": "theft_excess", "label": "Theft losses", "type": "text", "category": "EXCESS"},
                ],
                default_benefits={
                    "tp_persons": 10000000,
                    "tp_property": 30000000,
                    "towing": 100000,
                },
                default_clauses=["Including Special Perils", "No blame no excess"],
            )
            session.add(motor_product)

        # PRODUCT: DOMESTIC PACKAGE
        domestic_product = session.exec(select(Product).where(Product.name == "Domestic Package - HomeShield")).first()
        if not domestic_product:
            domestic_product = Product(
                insurer_id=old_mutual.id,
                name="Domestic Package - HomeShield",
                class_of_insurance="Domestic Package",
                form_schema=[
                    {"key": "location", "label": "Location", "type": "text", "category": "LOCATION"},
                    {"key": "construction", "label": "Construction", "type": "text", "category": "LOCATION"},
                    {"key": "value", "label": "Value Kshs.", "type": "number", "category": "LOCATION"},
                    {"key": "contents", "label": "Section B: (Contents)", "type": "number", "category": "INTEREST & SUM INSURED"},
                    {"key": "all_risks", "label": "Section C: (All Risks)", "type": "number", "category": "INTEREST & SUM INSURED"},
                    {"key": "owners_liability", "label": "Owners Liability", "type": "number", "category": "LIABILITIES"},
                    {"key": "occupiers_liability", "label": "Occupiers Liability", "type": "number", "category": "LIABILITIES"},
                ],
                default_benefits={
                    "owners_liability": 1000000,
                    "occupiers_liability": 1000000,
                },
                default_clauses=["Automatic reinstatement of loss", "Fire brigade"],
            )
            session.add(domestic_product)

        session.commit()
        logger.info("✅ Catalog Seeded with Old Mutual Products")

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
                    "tp_persons": 10000000,
                    "tp_property": 30000000,
                    "towing": 100000,
                    "own_damage_excess": "2.5% of value min 15k",
                    "theft_excess": "10% of vehicle value",
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
                special_clauses=["Including Special Perils", "No blame no excess"],
            )
            session.add(rn)
            session.commit()

        logger.info("✅ Mock Data Seeded Successfully")

        logger.info("✅ Mock Data Seeded Successfully")


if __name__ == "__main__":
    create_mock_data()
