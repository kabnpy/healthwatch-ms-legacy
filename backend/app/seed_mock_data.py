import logging
from datetime import date

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

        # Helper to create/update products
        def upsert_product(name: str, class_of_insurance: str, product_details: list[dict]):
            product = session.exec(select(Product).where(Product.name == name)).first()
            if not product:
                product = Product(
                    insurer_id=old_mutual.id,
                    name=name,
                    class_of_insurance=class_of_insurance,
                    product_details=product_details
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
        pa_details = [
            {"key": "occupation", "label": "Occupation", "type": "text", "field_type": "input", "section": "OCCUPATION"},
            {"key": "acc_death", "label": "Accidental Death", "type": "static", "field_type": "static", "section": "BENEFITS", "value": "Kshs. 500,000/-"},
            {"key": "perm_total_disability", "label": "Permanent Total Disablement", "type": "static", "field_type": "static", "section": "BENEFITS", "value": "Kshs. 500,000/-"},
            {"key": "hosp_cash", "label": "Hospital Cash", "type": "static", "field_type": "static", "section": "BENEFITS", "value": "Kshs. 1,000/-"},
            {"key": "ttd", "label": "Accidental temporary total disability", "type": "static", "field_type": "static", "section": "BENEFITS", "value": "Kshs. 5,000/- (Weekly benefits 104 weeks)"},
            {"key": "med_expenses", "label": "Accidental medical expenses", "type": "static", "field_type": "static", "section": "BENEFITS", "value": "Kshs. 70,000/-"},
            {"key": "appliances", "label": "Artificial appliances (Accidental Loss)", "type": "static", "field_type": "static", "section": "BENEFITS", "value": "Kshs. 10,000/-"},
            {"key": "funeral_grant", "label": "Last expense (Accidental Death)", "type": "static", "field_type": "static", "section": "BENEFITS", "value": "Kshs. 50,000/-"},
            {"key": "clause_24hr", "label": "24hour cover", "type": "static", "field_type": "static", "section": "SPECIAL CLAUSES", "value": "Including Piloting and Aircrew duties"},
            {"key": "clause_duty", "label": "Duty or pleasure", "type": "static", "field_type": "static", "section": "SPECIAL CLAUSES", "value": "Included"},
            {"key": "clause_worldwide", "label": "Worldwide limits", "type": "static", "field_type": "static", "section": "SPECIAL CLAUSES", "value": "Included"},
            {"key": "clause_disappearance", "label": "Disappearance clause", "type": "static", "field_type": "static", "section": "SPECIAL CLAUSES", "value": "Included"},
            {"key": "clause_age", "label": "Age limits 16-65 years", "type": "static", "field_type": "static", "section": "SPECIAL CLAUSES", "value": "Included"},
            {"key": "excl_racing", "label": "Racing Risks", "type": "static", "field_type": "static", "section": "EXCLUDED RISKS", "value": "Included"},
            {"key": "excl_winter", "label": "Winter sports", "type": "static", "field_type": "static", "section": "EXCLUDED RISKS", "value": "Included"},
            {"key": "excl_suicide", "label": "Suicide or attempted suicide", "type": "static", "field_type": "static", "section": "EXCLUDED RISKS", "value": "Included"},
            {"key": "excl_war", "label": "War and kindred risks", "type": "static", "field_type": "static", "section": "EXCLUDED RISKS", "value": "Included"},
            {"key": "excl_liquor", "label": "Influence of intoxicating Liquor or drugs", "type": "static", "field_type": "static", "section": "EXCLUDED RISKS", "value": "Included"},
        ]
        pa_product = upsert_product("Maxpac Personal Accident", "Personal Accident", pa_details)

        # PRODUCT: MOTOR PRIVATE
        motor_details = [
            {"key": "reg_no", "label": "Reg. No", "type": "text", "field_type": "input", "section": "VEHICLE DETAILS"},
            {"key": "make", "label": "Make", "type": "text", "field_type": "input", "section": "VEHICLE DETAILS"},
            {"key": "year", "label": "Year", "type": "number", "field_type": "input", "section": "VEHICLE DETAILS"},
            {"key": "value", "label": "Value Kshs.", "type": "number", "field_type": "input", "section": "VEHICLE DETAILS", "pricing_type": "percentage", "pricing_value": 3.25},
            {"key": "tp_persons", "label": "Third Party Persons", "type": "static", "field_type": "static", "section": "HIGH-END BENEFITS & LIMITS", "value": "Kshs. 10,000,000.00"},
            {"key": "tp_property", "label": "Third Party Property", "type": "static", "field_type": "static", "section": "HIGH-END BENEFITS & LIMITS", "value": "Kshs. 30,000,000.00"},
            {"key": "pass_liability", "label": "Passengers Legal Liability", "type": "static", "field_type": "static", "section": "HIGH-END BENEFITS & LIMITS", "value": "Kshs. 4,000,000 per person and Kshs. 20,000,000.00 per event"},
            {"key": "towing", "label": "Towing & Recovery", "type": "static", "field_type": "static", "section": "HIGH-END BENEFITS & LIMITS", "value": "Kshs. 100,000.00"},
            {"key": "repair_limit", "label": "Authorized repair limit", "type": "static", "field_type": "static", "section": "HIGH-END BENEFITS & LIMITS", "value": "Kshs. 100,000.00"},
            {"key": "windscreen", "label": "Windscreen/Window glass", "type": "static", "field_type": "static", "section": "HIGH-END BENEFITS & LIMITS", "value": "Fully covered on replacement cost"},
            {"key": "mirrors", "label": "Side mirrors & Housing", "type": "static", "field_type": "static", "section": "HIGH-END BENEFITS & LIMITS", "value": "Replacement Cost Max Kshs. 100,000.00"},
            {"key": "exc_od", "label": "Own Damage and Partial", "type": "static", "field_type": "static", "section": "EXCESS", "value": "2.5% of value minimum Kshs. 15,000/- Max Kshs. 100,000.00"},
            {"key": "exc_tp_damage", "label": "Third Party damage claims", "type": "static", "field_type": "static", "section": "EXCESS", "value": "Kshs. 5,000.00"},
            {"key": "exc_tp_injury", "label": "Third Party Injury", "type": "static", "field_type": "static", "section": "EXCESS", "value": "Nil"},
            {"key": "clause_perils", "label": "Including Special Perils", "type": "static", "field_type": "static", "section": "SPECIAL CLAUSES", "value": "Included"},
            {"key": "clause_riot", "label": "Including riot, Strike and civil commotion", "type": "static", "field_type": "static", "section": "SPECIAL CLAUSES", "value": "Included"},
        ]
        motor_product = upsert_product("Motor Private - Comprehensive", "Motor Private", motor_details)

        # PRODUCT: DOMESTIC PACKAGE
        domestic_details = [
            {"key": "location", "label": "Location", "type": "text", "field_type": "input", "section": "LOCATION"},
            {"key": "value", "label": "Value Kshs.", "type": "number", "field_type": "input", "section": "LOCATION", "pricing_type": "percentage", "pricing_value": 1.5},
            {"key": "sec_b", "label": "Section B: (Contents)", "type": "static", "field_type": "static", "section": "INTEREST & SUM INSURED", "value": "Kshs. 6,430,000/- (As per the attached Schedule)"},
            {"key": "sec_c", "label": "Section C: (All Risks)", "type": "static", "field_type": "static", "section": "INTEREST & SUM INSURED", "value": "Kshs. 450,000/- (As per the attached Schedule)"},
        ]
        domestic_product = upsert_product("Domestic Package - HomeShield", "Domestic Package", domestic_details)

        session.commit()

        # 2. CLIENT (Agnes Njoki Mwangi)
        client = session.exec(select(Client).where(Client.kra_pin == "A001158997L")).first()
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

        # 3. MOTOR POLICY
        policy = session.exec(select(Policy).where(Policy.policy_number == "010/070/1/012473/2017")).first()
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

        # 4. MOTOR RISK ITEM
        item = session.exec(select(RiskItem).where(RiskItem.policy_id == policy.id)).first()
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
        else:
            # Update item snapshot details if needed
            item.risk_details = {
                "reg_no": "KCM 780L",
                "make": "Toyota Landcruiser Prado",
                "year": 2016,
                "value": 4700000.0,
            }
            session.add(item)

        # 5. MOTOR RISK NOTE
        rn = session.exec(select(RiskNote).where(RiskNote.policy_id == policy.id)).first()
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
        else:
            # IMPORTANT: Update snapshot to reflect latest product fields
            rn.items_snapshot = {
                "items": [
                    {
                        "name": motor_product.name,
                        "description": item.description,
                        "cover": item.cover_description,
                        "premium": item.total_premium,
                        "details": item.risk_details,
                    }
                ]
            }
            session.add(rn)
            session.commit()

        logger.info("✅ Mock Data Seeded & Synchronized Successfully")


if __name__ == "__main__":
    create_mock_data()