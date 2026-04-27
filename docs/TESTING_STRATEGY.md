# Testing Strategy

## 1. Overview
Our testing strategy is designed to ensure financial integrity, document accuracy, and system reliability across the full stack. We use a three-tiered approach.

## 2. Test Tiers

### Tier 1: Standalone Unit Tests (Fast & Isolated)
- **Location:** `backend/tests/standalone/`
- **Scope:** Business logic that does not require a database connection (e.g., PDF generation, Middleware, Rating Engine calculations).
- **Tooling:** `pytest`, `unittest.mock`.
- **Command:** `cd backend && uv run pytest tests/standalone/`

### Tier 2: Integration Tests (Database Dependent)
- **Location:** `backend/tests/` (excluding `standalone/`)
- **Scope:** CRUD operations, API endpoints, and complex workflows that interact with PostgreSQL.
- **Tooling:** `pytest`, `TestClient`, `SQLModel`.
- **Note:** Requires a live test database (configured via `.env`).
- **Command:** `cd backend && uv run pytest tests/`

### Tier 3: End-to-End (E2E) Tests (Browser Based)
- **Location:** `frontend/tests/`
- **Scope:** Critical user journeys (Login, Policy Issuance, PDF Viewing).
- **Tooling:** `Playwright`.
- **Command:** `cd frontend && npx playwright test`

## 3. Coverage Priorities
1. **Financial Precision:** Every calculation (levies, commissions, taxes) must have a Tier 1 or Tier 2 test.
2. **Document Snapshots:** PDF generation logic must be verified for structure and presence of key data points.
3. **Security:** RBAC (Role Based Access Control) is verified in `backend/tests/api/routes/test_security_audit.py`.

## 4. Continuous Integration (CI)
- Tier 1 tests MUST run on every PR and pass before merging.
- Tier 2 and Tier 3 tests run on the staging environment before production deployment.
