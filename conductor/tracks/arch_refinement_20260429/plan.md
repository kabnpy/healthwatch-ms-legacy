# Implementation Plan: System Architecture Refinement & Hardening

## Phase 1: Backend Decoupling (Strict Services)
- [x] Task: Refactor Product Model
    - [x] Create `backend/app/services/product.py` and implement `ProductService`.
    - [x] Move `validate_risk_details` and `calculate_premium` from `Product` model to `ProductService`.
    - [x] Update `backend/app/api/routes/policies.py` and `backend/app/seed_mock_data.py` to use `ProductService`.
- [x] Task: Refactor Policy & RiskNote Models
    - [x] Audit `Policy` and `RiskNote` models for lingering business logic.
    - [x] Consolidate orchestration into `PolicyService` and `RiskNoteService` as needed.
- [x] Task: Verify Service Layer Unit Tests
    - [x] Update existing tests in `backend/tests/test_rating_service.py` and others to reflect the new service structure.
    - [x] Ensure all backend tests pass.
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Frontend Utilities & Error Boundaries
- [x] Task: Centralize Document Service
    - [x] Create `frontend/src/services/document.ts`.
    - [x] Implement URL construction and `downloadAuthenticatedFile` orchestration.
    - [x] Update `DocumentViewer.tsx` and `risk-notes.$id.tsx` to use this service.
- [x] Task: Standardize Error Boundaries
    - [x] Create specialized Error Fallback components for different layout areas.
    - [x] Audit and wrap major routes with consistent `ErrorBoundary` treatments.
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Frontend Route Modularization
- [ ] Task: Decompose Policy Dashboard
    - [x] Extract `ActionToolbar` into a separate component.
    - [ ] Extract `TransactionHistory` timeline into a separate component.
    - [ ] Extract `PolicyFinancialOverview` and `ActionToolbar`.
    - [ ] Refactor `clients.$clientId.policies.$policyId.tsx` to orchestrate these sub-components.
- [ ] Task: Audit and Decompose Other "God" Files
    - [ ] Review `NewPolicyWizard.tsx` and `ClientInvoices.tsx` for modularization opportunities.
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: E2E Test Suite (Playwright)
- [ ] Task: Setup E2E Foundation
    - [ ] Configure Playwright fixtures for authenticated user states.
- [ ] Task: Implement Policy Wizard E2E
    - [ ] Write test for full "New Policy" flow.
- [ ] Task: Implement Renewal Workflow E2E
    - [ ] Write test for renewal invitation and document viewing.
- [ ] Task: Implement Document Actions E2E
    - [ ] Write test for print and download triggers.
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5: Final Validation & Hardening
- [ ] Task: Full System Audit
    - [ ] Run all formatters and linters.
    - [ ] Verify final code coverage (>80%).
- [ ] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)
