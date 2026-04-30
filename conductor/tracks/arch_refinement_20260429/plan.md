# Implementation Plan: System Architecture Refinement & Hardening

## Phase 1: Backend Decoupling (Strict Services)
- [ ] Task: Refactor Product Model
    - [ ] Create `backend/app/services/product.py` and implement `ProductService`.
    - [ ] Move `validate_risk_details` and `calculate_premium` from `Product` model to `ProductService`.
    - [ ] Update `backend/app/api/routes/policies.py` and `backend/app/seed_mock_data.py` to use `ProductService`.
- [ ] Task: Refactor Policy & RiskNote Models
    - [ ] Audit `Policy` and `RiskNote` models for lingering business logic.
    - [ ] Consolidate orchestration into `PolicyService` and `RiskNoteService` as needed.
- [ ] Task: Verify Service Layer Unit Tests
    - [ ] Update existing tests in `backend/tests/test_rating_service.py` and others to reflect the new service structure.
    - [ ] Ensure all backend tests pass.
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Frontend Utilities & Error Boundaries
- [ ] Task: Centralize Document Service
    - [ ] Create `frontend/src/services/document.ts`.
    - [ ] Implement URL construction and `downloadAuthenticatedFile` orchestration.
    - [ ] Update `DocumentViewer.tsx` and `risk-notes.$id.tsx` to use this service.
- [ ] Task: Standardize Error Boundaries
    - [ ] Create specialized Error Fallback components for different layout areas.
    - [ ] Audit and wrap major routes with consistent `ErrorBoundary` treatments.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Frontend Route Modularization
- [ ] Task: Decompose Policy Dashboard
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
