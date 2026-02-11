import logging
from datetime import date
from typing import Any

from sqlmodel import Session, select

from app.core.db import engine
from app.models import (
    Client,
    Insurer,
    Policy,
    Product,
    RiskNote,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_mock_data() -> None:
    with Session(engine) as session:
        # 1. SETUP THE CATALOG
        old_mutual = session.exec(
            select(Insurer).where(
                Insurer.name == "Old Mutual General Insurance Kenya Ltd."
            )
        ).first()
        if not old_mutual:
            old_mutual = Insurer(
                name="Old Mutual General Insurance Kenya Ltd.",
                email="info@oldmutual.co.ke",
            )
            session.add(old_mutual)
            session.commit()
            session.refresh(old_mutual)

        # Helper to create/update products
        def upsert_product(
            name: str,
            class_of_insurance: str,
            product_details: dict[str, Any],
        ) -> Product:
            product = session.exec(select(Product).where(Product.name == name)).first()
            if not product:
                product = Product(
                    insurer_id=old_mutual.id,
                    name=name,
                    class_of_insurance=class_of_insurance,
                    product_details=product_details,
                )
                session.add(product)
                logger.info(f"Created product: {name}")
            else:
                product.product_details = product_details
                product.class_of_insurance = class_of_insurance
                session.add(product)
                logger.info(f"Updated product: {name}")
            return product

        # PRODUCT: PERSONAL ACCIDENT
        pa_details = {
            "OCCUPATION": {"Occupation": "<<text>>"},
            "BENEFITS": {
                "Accidental Death": "Kshs. 500,000/-",
                "Permanent Total Disablement": "Kshs. 500,000/-",
                "Hospital Cash": "Kshs. 1,000/-",
                "Accidental temporary total disability": "Kshs. 5,000/- (Weekly benefits 104 weeks)",
                "Accidental medical expenses": "Kshs. 70,000/-",
                "Artificial appliances (Accidental Loss)": "Kshs. 10,000/-",
                "Last expense (Accidental Death)": "Kshs. 50,000/-",
            },
            "SPECIAL CLAUSES": [
                "24hour cover including Piloting and Aircrew duties",
                "Duty or pleasure",
                "Worldwide limits",
                "Disappearance clause",
                "Age limits 16-65 years",
            ],
            "EXCLUDED RISKS": [
                "Racing Risks",
                "Winter sports",
                "Suicide or attempted suicide",
                "War and kindred risks",
                "Influence of intoxicating Liquor or drugs",
            ],
        }
        upsert_product("Maxpac Personal Accident", "Personal Accident", pa_details)

        # PRODUCT: MOTOR PRIVATE
        motor_details = {
            "VEHICLE DETAILS": {
                "Reg. No": "<<text>>",
                "Make": "<<text>>",
                "Year": "<<number>>",
                "Value Kshs.": "<<number>>",
            },
            "HIGH-END BENEFITS & LIMITS": {
                "Third Party Persons": "Kshs. 10,000,000.00",
                "Third Party Property": "Kshs. 30,000,000.00",
                "Passengers Legal Liability": "Kshs. 4,000,000 per person and Kshs. 20,000,000.00 per event",
                "Towing & Recovery": "Kshs. 100,000.00",
                "Authorized repair limit": "Kshs. 100,000.00",
                "Windscreen/Window glass": "Fully covered on replacement cost",
                "Side mirrors & Housing": "Replacement Cost Max Kshs. 100,000.00",
            },
            "EXCESS": {
                "Own Damage and Partial": "2.5% of value minimum Kshs. 15,000/- Max Kshs. 100,000.00",
                "Third Party damage claims": "Kshs. 5,000.00",
                "Third Party Injury": "Nil",
            },
            "SPECIAL CLAUSES": [
                "Including Special Perils",
                "Including riot, Strike and civil commotion",
            ],
        }
        motor_product = upsert_product(
            "Motor Private - Comprehensive", "Motor Private", motor_details
        )

        # PRODUCT: DOMESTIC PACKAGE
        domestic_details = {
            "LOCATION": {"Location": "<<text>>", "Value Kshs.": "<<number>>"},
            "INTEREST & SUM INSURED": {
                "Section B: (Contents)": "Kshs. 6,430,000/- (As per the attached Schedule)",
                "Section C: (All Risks)": "Kshs. 450,000/- (As per the attached Schedule)",
            },
        }
        upsert_product(
            "Domestic Package - HomeShield", "Domestic Package", domestic_details
        )

        session.commit()

        # 2. CLIENT (Agnes Njoki Mwangi)
        client = session.exec(
            select(Client).where(Client.kra_pin == "A001158997L")
        ).first()
        if not client:
            client = Client(
                name="Agnes Njoki Mwangi",
                kra_pin="A001158997L",
                phone="0733980566",
                postal_number="11908",
                postal_code="00100",
                town="Nairobi",
                email="agnes@example.com",
            )
            session.add(client)
            session.commit()
            session.refresh(client)

        # 3. MOTOR POLICY
        policy = session.exec(
            select(Policy).where(Policy.policy_number == "010/070/1/012473/2017")
        ).first()
        if not policy:
            policy = Policy(
                policy_number="010/070/1/012473/2017",
                client_id=client.id,
                product_id=motor_product.id,
                status="Active",
                start_date=date(2025, 8, 2),
                end_date=date(2026, 8, 1),
                description="KCM 780L - Toyota Landcruiser Prado",
                total_premium=153438.0,
                premium_breakdown={
                    "basic": 152750.0,
                    "levies": {"trainingLevy": 306.0, "phcf": 382.0},
                },
                risk_details={
                    "VEHICLE DETAILS": {
                        "Reg. No": "KCM 780L",
                        "Make": "Toyota Landcruiser Prado",
                        "Year": 2016,
                        "Value Kshs.": 4700000.0,
                    }
                },
            )
            session.add(policy)
            session.commit()
            session.refresh(policy)
        else:
            # Update policy details if needed
            policy.start_date = date(2025, 8, 2)
            policy.end_date = date(2026, 8, 1)
            policy.description = "KCM 780L - Toyota Landcruiser Prado"
            policy.total_premium = 153438.0
            policy.premium_breakdown = {
                "basic": 152750.0,
                "levies": {"trainingLevy": 306.0, "phcf": 382.0},
            }
            policy.risk_details = {
                "VEHICLE DETAILS": {
                    "Reg. No": "KCM 780L",
                    "Make": "Toyota Landcruiser Prado",
                    "Year": 2016,
                    "Value Kshs.": 4700000.0,
                }
            }
            session.add(policy)
            session.commit()

        # 5. MOTOR RISK NOTE
        rn = session.exec(
            select(RiskNote).where(RiskNote.policy_id == policy.id)
        ).first()
        
        # Snapshot helper
        def get_policy_snapshot(p: Policy):
            dump = p.model_dump()
            # Convert dates to strings for JSON
            if dump.get("start_date"): dump["start_date"] = str(dump["start_date"])
            if dump.get("end_date"): dump["end_date"] = str(dump["end_date"])
            if dump.get("created_at"): dump["created_at"] = str(dump["created_at"])
            # Remove UUIDs if needed, or keep as strings
            dump["id"] = str(dump["id"])
            dump["client_id"] = str(dump["client_id"])
            if dump.get("product_id"): dump["product_id"] = str(dump["product_id"])
            return dump

        if not rn:
            rn = RiskNote(
                policy_id=policy.id,
                risk_note_number="RSK-SEED-001",
                transaction_type="New Business",
                invoice_number="HW-MOT-001",
                start_date=date(2025, 8, 2),
                end_date=date(2026, 8, 1),
                net_premium=152750.0,
                taxes={"trainingLevy": 306.0, "phcf": 382.0},
                commission_amount=15275.0,
                total_amount=153438.0,
                status="Active",
                policy_snapshot=get_policy_snapshot(policy),
                special_clauses=[],
            )
            session.add(rn)
            session.commit()
        else:
            # IMPORTANT: Update snapshot to reflect latest policy fields
            rn.policy_snapshot = get_policy_snapshot(policy)
            session.add(rn)
            session.commit()

        logger.info("✅ Mock Data Seeded & Synchronized Successfully")


if __name__ == "__main__":
    create_mock_data()
