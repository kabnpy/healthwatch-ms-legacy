import logging
from datetime import date
from typing import Any

from sqlmodel import Session, select

from app.core.db import engine
from app.models import (
    Client,
    Insurer,
    Policy,
    PolicyCreate,
    PricingStrategy,
    Product,
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
            pricing_strategy: PricingStrategy = PricingStrategy.PERCENTAGE,
            pricing_rules: dict[str, Any] | None = None,
        ) -> Product:
            product = session.exec(select(Product).where(Product.name == name)).first()
            if not product:
                product = Product(
                    insurer_id=old_mutual.id,
                    name=name,
                    class_of_insurance=class_of_insurance,
                    product_details=product_details,
                    pricing_strategy=pricing_strategy,
                    pricing_rules=pricing_rules or {},
                )
                session.add(product)
                logger.info(f"Created product: {name}")
            else:
                product.product_details = product_details
                product.class_of_insurance = class_of_insurance
                product.pricing_strategy = pricing_strategy
                product.pricing_rules = pricing_rules or {}
                session.add(product)
                logger.info(f"Updated product: {name}")
            session.commit()
            session.refresh(product)
            return product

        # PRODUCT: MOTOR PRIVATE
        motor_details = {
            "vehicle_details": {
                "registration_number": "<<text>>",
                "make": "<<text>>",
                "year_of_manufacture": "<<number>>",
                "sum_insured": "<<number>>",
            },
            "added_benefits": {
                "pvt": "<<boolean>>",
                "excess_protector": "<<boolean>>",
                "om_rescue_plus": "<<boolean>>",
                "passenger_liability": "<<boolean>>",
            },
            "excesses": {
                "Own Damage and Partial": "2.5% of value minimum Kshs. 15,000/- Max Kshs. 100,000.00",
                "Third Party damage claims": "Kshs. 5,000.00",
                "Third Party Injury": "Nil",
                "Total Theft losses with antitheft device": "10% of vehicle value minimum Kshs. 20,000/-",
                "Total Theft losses without antitheft device": "20% of vehicle value minimum Kshs. 20,000/-",
                "Total Theft losses for vehicles with tracking device": "2.5% of vehicle value minimum Kshs. 20,000/-",
                "Young and novice drivers": "Additional Kshs. 7,500.00 Each (under 21 years / Less than 1 year)",
            },
            "special_clauses": [
                "Including special perils",
                "Including Kenya jurisdiction",
            ],
        }
        motor_pricing_rules = {
            "tiers": [
                {"max": 1500000, "rate": 5.0, "min": 60000},
                {"max": 2500000, "rate": 4.0, "min": 75000},
                {"max": 3000000, "rate": 3.5, "min": 100000},
                {"max": 5000000, "rate": 3.25, "min": 0},
                {"max": None, "rate": 3.0, "min": 0},
            ]
        }
        motor_product = upsert_product(
            "Motor Private - Comprehensive",
            "Motor Private",
            motor_details,
            pricing_strategy=PricingStrategy.FIXED_TIERED,
            pricing_rules=motor_pricing_rules,
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
            cover_snapshot = {
                "vehicle": {
                    "registration_number": "KCM 780L",
                    "make": "Toyota",
                    "year_of_manufacture": 2016,
                    "sum_insured": 4700000.0,
                },
                "extensions": {"pvt": True, "excess_protector": True},
                "benefits_and_limits": "Standard Comprehensive Benefits...",
                "excesses": "Standard Motor Private Excesses...",
                "special_clauses": "Subject to annual valuation...",
            }

            policy_in = PolicyCreate(
                policy_number="010/070/1/012473/2017",
                client_id=client.id,
                product_id=motor_product.id,
                status="Active",
                inception_date=start_date,
            )

            policy = policy_service.create_policy(
                session=session,
                policy_in=policy_in,
                cover_snapshot=cover_snapshot,
                coverage_start=start_date,
                coverage_end=end_date,
            )

            logger.info(
                f"Created atomic policy and initial RiskNote: {policy.policy_number}"
            )

        logger.info("✅ Mock Data Seeded & Synchronized Successfully")


if __name__ == "__main__":
    create_mock_data()
