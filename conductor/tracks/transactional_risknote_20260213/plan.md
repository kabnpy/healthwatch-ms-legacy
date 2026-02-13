# Implementation Plan: Transactional RiskNote Architectural Refactor

## Phase 1: Database and Model Refactoring
Establish the new schema by removing duplicated fields from `Policy` and ensuring `RiskNote` contains the full state.

- [ ] Task: **Write Tests for Updated Models**: Create tests that verify the new schema constraints and the immutability of issued `RiskNotes`.
- [ ] Task: **Update backend/app/models/insurance/policy.py**: Remove `risk_details`, `total_premium`, etc., and implement computed properties to read from `risk_notes`.
- [ ] Task: **Update backend/app/models/insurance/risk_note.py**: Ensure `policy_snapshot` JSON field is correctly typed and indexed.
- [ ] Task: **Database Reset and Migration**: Perform a destructive reset of the local database and generate a fresh Alembic migration.
- [ ] Task: **Conductor - User Manual Verification 'Phase 1: Database and Model Refactoring' (Protocol in workflow.md)**

## Phase 2: Service and CRUD Layer Refactoring
Refactor the backend logic to handle the atomic creation of policies and risk notes.

- [ ] Task: **Write Tests for PolicyService**: Define tests for atomic policy creation and endorsement flows using the new pattern.
- [ ] Task: **Refactor PolicyService.create_policy**: Update the service to create a `Policy` container and an initial `RiskNote` in one atomic transaction.
- [ ] Task: **Refactor Endorsement Logic**: Ensure updates to policy details always result in a new `RiskNote` rather than a `Policy` update.
- [ ] Task: **Verify CRUD Integrity**: Ensure `backend/app/crud/` functions for Policy and RiskNote respect the new schema.
- [ ] Task: **Conductor - User Manual Verification 'Phase 2: Service and CRUD Layer Refactoring' (Protocol in workflow.md)**

## Phase 3: Frontend Data Integration
Update the React application to correctly fetch and display policy data from the transactional snapshots.

- [ ] Task: **Update API Client and Hooks**: Refactor TanStack Query hooks in `frontend/src/hooks/useInsurance.ts` to reflect the schema changes.
- [ ] Task: **Update Policy Dashboard and Details**: Refactor components in `frontend/src/routes/` to read current state from `latest_risk_note`.
- [ ] Task: **Refactor New Policy Wizard**: Update `NewPolicyWizard.tsx` to handle the new atomic creation flow and validation.
- [ ] Task: **Conductor - User Manual Verification 'Phase 3: Frontend Data Integration' (Protocol in workflow.md)**

## Phase 4: Data Seeding and Final Verification
Finalize the refactor by updating the seed data and performing a full system validation.

- [ ] Task: **Update backend/app/seed_mock_data.py**: Rewrite the mock data generation script to align with the new transactional pattern.
- [ ] Task: **Final Integration Testing**: Run the complete `pytest` and `playwright` suites to ensure system-wide stability.
- [ ] Task: **Conductor - User Manual Verification 'Phase 4: Data Seeding and Final Verification' (Protocol in workflow.md)**
