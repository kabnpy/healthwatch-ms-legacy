# Implementation Plan: Transactional RiskNote Architectural Refactor

## Phase 1: Database and Model Refactoring [checkpoint: 33bf144]
Establish the new schema by removing duplicated fields from `Policy` and ensuring `RiskNote` contains the full state.

- [x] Task: **Write Tests for Updated Models**: Create tests that verify the new schema constraints and the immutability of issued `RiskNotes`. (879c037)
- [x] Task: **Update backend/app/models/insurance/policy.py**: Remove `risk_details`, `total_premium`, etc., and implement computed properties to read from `risk_notes`. (879c037)
- [x] Task: **Update backend/app/models/insurance/risk_note.py**: Ensure `policy_snapshot` JSON field is correctly typed and indexed. (879c037)
- [x] Task: **Database Reset and Migration**: Perform a destructive reset of the local database and generate a fresh Alembic migration. (879c037)
- [ ] Task: **Conductor - User Manual Verification 'Phase 1: Database and Model Refactoring' (Protocol in workflow.md)**

## Phase 2: Service and CRUD Layer Refactoring [checkpoint: f0e6d1a]
Refactor the backend logic to handle the atomic creation of policies and risk notes.

- [x] Task: **Write Tests for PolicyService**: Define tests for atomic policy creation and endorsement flows using the new pattern. (e3f0b3f)
- [x] Task: **Refactor PolicyService.create_policy**: Update the service to create a `Policy` container and an initial `RiskNote` in one atomic transaction. (e3f0b3f)
- [x] Task: **Refactor Endorsement Logic**: Ensure updates to policy details always result in a new `RiskNote` rather than a `Policy` update. (e3f0b3f)
- [x] Task: **Verify CRUD Integrity**: Ensure `backend/app/crud/` functions for Policy and RiskNote respect the new schema. (e3f0b3f)
- [ ] Task: **Conductor - User Manual Verification 'Phase 2: Service and CRUD Layer Refactoring' (Protocol in workflow.md)**

## Phase 3: Frontend Data Integration [checkpoint: 30bc787]
Update the React application to correctly fetch and display policy data from the transactional snapshots.

- [x] Task: **Update API Client and Hooks**: Refactor TanStack Query hooks in `frontend/src/hooks/useInsurance.ts` to reflect the schema changes. (30bc787)
- [x] Task: **Update Policy Dashboard and Details**: Refactor components in `frontend/src/routes/` to read current state from `latest_risk_note`. (30bc787)
- [x] Task: **Refactor New Policy Wizard**: Update `NewPolicyWizard.tsx` to handle the new atomic creation flow and validation. (30bc787)
- [ ] Task: **Conductor - User Manual Verification 'Phase 3: Frontend Data Integration' (Protocol in workflow.md)**

## Phase 4: Data Seeding and Final Verification [checkpoint: 1610efc]
Finalize the refactor by updating the seed data and performing a full system validation.

- [x] Task: **Update backend/app/seed_mock_data.py**: Rewrite the mock data generation script to align with the new transactional pattern. (1610efc)
- [x] Task: **Final Integration Testing**: Run the complete `pytest` and `playwright` suites to ensure system-wide stability. (1610efc)
- [ ] Task: **Conductor - User Manual Verification 'Phase 4: Data Seeding and Final Verification' (Protocol in workflow.md)**

## Phase: Review Fixes
- [x] Task: Apply review suggestions (b9b9a29)
