import uuid
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from tests.utils.insurance import create_random_product


def test_get_policy_quote_motor_private(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    product = create_random_product(db, class_of_insurance="Motor Private")
    data = {
        "product_id": str(product.id),
        "risk_details": {
            "VEHICLE DETAILS": {
                "Value Kshs.": 1000000
            },
            "EXTENSIONS": {
                "pvt": True,
                "excess_protector": True
            }
        }
    }
    response = client.post(
        f"{settings.API_V1_STR}/policies/quote",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert "breakdown" in content
    breakdown = content["breakdown"]
    assert breakdown["type"] == "motor"
    # Basic: 1,000,000 * 0.0325 = 32,500
    # PVT: 1,000,000 * 0.0025 = 2,500
    # EP: 1,000,000 * 0.0025 = 2,500
    # Net: 32,500 + 2,500 + 2,500 = 37,500
    assert float(breakdown["net_premium"]) == 37500.0
    assert "taxes" in breakdown
    assert "training_levy" in breakdown["taxes"]
    assert "phcf" in breakdown["taxes"]
    assert "stamp_duty" in breakdown["taxes"]
    assert len(breakdown["benefits"]) == 2

def test_get_policy_quote_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    import uuid
    data = {
        "product_id": str(uuid.uuid4()),
        "risk_details": {}
    }
    response = client.post(
        f"{settings.API_V1_STR}/policies/quote",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404


def test_create_policy_with_breakdown(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    from datetime import date, timedelta
    from tests.utils.client import create_random_client
    
    db_client = create_random_client(db)
    product = create_random_product(db, class_of_insurance="Motor Private")
    
    data = {
        "policy_number": f"POL-{uuid.uuid4().hex[:6].upper()}",
        "client_id": str(db_client.id),
        "product_id": str(product.id),
        "coverage_start": str(date.today()),
        "coverage_end": str(date.today() + timedelta(days=365)),
        "risk_details": {
            "VEHICLE DETAILS": {
                "Reg. No": "KAA 001A",
                "Make": "Toyota",
                "Year": 2020,
                "Value Kshs.": 1000000
            }
        }
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/policies/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["policy_number"] == data["policy_number"]
    
    # Check if risk note was created with breakdown
    policy_id = content["id"]
    rn_response = client.get(
        f"{settings.API_V1_STR}/policies/{policy_id}/risk-notes",
        headers=superuser_token_headers,
    )
    assert rn_response.status_code == 200
    rn_content = rn_response.json()
    assert rn_content["count"] > 0
    risk_note = rn_content["data"][0]
    
    assert "financial_breakdown" in risk_note
    breakdown = risk_note["financial_breakdown"]
    assert breakdown["type"] == "motor"
    assert float(breakdown["net_premium"]) == 32500.0 # 3.25% of 1M


def test_read_policies(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    from tests.utils.insurance import create_random_policy
    create_random_policy(db)
    
    response = client.get(
        f"{settings.API_V1_STR}/policies/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["count"] > 0


def test_read_policy(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    from tests.utils.insurance import create_random_policy
    policy = create_random_policy(db)
    
    response = client.get(
        f"{settings.API_V1_STR}/policies/{policy.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["policy_number"] == policy.policy_number


def test_update_policy(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    from tests.utils.insurance import create_random_policy
    policy = create_random_policy(db)
    new_policy_number = f"UPDATED-{uuid.uuid4().hex[:6].upper()}"
    
    data = {"policy_number": new_policy_number}
    response = client.put(
        f"{settings.API_V1_STR}/policies/{policy.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["policy_number"] == new_policy_number


def test_delete_policy(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    from tests.utils.insurance import create_random_policy
    policy = create_random_policy(db)
    
    response = client.delete(
        f"{settings.API_V1_STR}/policies/{policy.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    
    response = client.get(
        f"{settings.API_V1_STR}/policies/{policy.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
