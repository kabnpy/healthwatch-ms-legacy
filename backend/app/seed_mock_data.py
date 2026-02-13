import logging
from datetime import date, timedelta
from decimal import Decimal
from typing import Any

from sqlmodel import Session, select

from app.core.db import engine
from app.models import (
    Client,
    Insurer,
    Policy,
    Product,
    RiskNote,
    PolicyCreateExtended,
)
from app.services.policy import policy_service

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
            session.commit()
            session.refresh(product)
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
            "EXCESS": {
                "Own Damage and Partial": "2.5% of value minimum Kshs. 15,000/- Max Kshs. 100,000.00",
                "Third Party damage claims": "Kshs. 5,000.00",
                "Third Party Injury": "Nil",
            },
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
            start_date = date(2025, 8, 2)
            end_date = date(2026, 8, 1)
            risk_details = {
                "VEHICLE DETAILS": {
                    "Reg. No": "KCM 780L",
                    "Make": "Toyota Landcruiser Prado",
                    "Year": 2016,
                    "Value Kshs.": 4700000.0,
                }
            }
            
            policy_in = PolicyCreateExtended(
                policy_number="010/070/1/012473/2017",
                client_id=client.id,
                product_id=motor_product.id,
                status="Active",
                inception_date=start_date,
                coverage_start=start_date,
                coverage_end=end_date,
                risk_details=risk_details
            )
            
            policy = policy_service.create_policy(
                session=session,
                policy_in=policy_in,
                risk_details=risk_details,
                coverage_start=start_date,
                coverage_end=end_date
            )
            
            logger.info(f"Created atomic policy and initial RiskNote: {policy.policy_number}")
            
            # 4. ADD AN ENDORSEMENT
            # Increase value 3 months later
            new_risk_details = {
                "VEHICLE DETAILS": {
                    "Reg. No": "KCM 780L",
                    "Make": "Toyota Landcruiser Prado",
                    "Year": 2016,
                    "Value Kshs.": 5000000.0,
                }
            }
            
            endorsement_rn = policy_service.create_endorsement(
                session=session,
                policy_id=policy.id,
                updated_risk_details=new_risk_details,
                change_description="Increased vehicle value to 5M"
            )
            logger.info(f"Created endorsement RiskNote: {endorsement_rn.risk_note_number}")

        logger.info("✅ Mock Data Seeded & Synchronized Successfully")


if __name__ == "__main__":
    create_mock_data()
