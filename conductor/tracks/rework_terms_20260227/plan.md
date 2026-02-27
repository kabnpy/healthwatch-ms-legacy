# Implementation Plan: Rework Cover Snapshot Terms

## Phase 0: Setup & Branching

- [x] Task: Create a new feature branch for the rework: `feat/rework-cover-terms`.
- [~] Task: Confirm current state and ensure all tests pass on the new branch.

## Phase 0.1: Fix Base Tests

- [x] Task: Update backend tests to correctly use `RiskNote.cover_snapshot` instead of `Policy.risk_details`.
- [x] Task: Resolve `TypeError: PolicyService.create_policy() got an unexpected keyword argument 'risk_details'`.
- [x] Task: Fix frontend Vitest configuration to ignore Playwright `.spec.ts` files.
- [x] Task: Ensure all tests pass.

## Phase 1: Backend Model & Schema Refactor

- [ ] Task: Update `RiskNote` and `Policy` schemas in `backend/app/schemas.py` to include the new `terms` object within `cover_snapshot`.
- [ ] Task: Refactor the `Policy` and `RiskNote` models in `backend/app/models.py` to support the new `terms` structure.
- [ ] Task: Write failing unit tests in `backend/tests/` to verify the updated schemas and models.
- [ ] Task: Implement changes to ensure tests pass.
- [ ] Task: Conductor - User Manual Verification 'Backend Model Refactor' (Protocol in workflow.md)

## Phase 2: Data Migration

- [ ] Task: Create an Alembic migration script to convert existing structured terms into the new text-based format for all active policies.
- [ ] Task: Write a test script to verify the migration on a copy of the production-like database.
- [ ] Task: Execute the migration and confirm data integrity.
- [ ] Task: Conductor - User Manual Verification 'Data Migration' (Protocol in workflow.md)

## Phase 3: Frontend UI Updates

- [ ] Task: Update the frontend API client using `scripts/generate-client.sh`.
- [ ] Task: Refactor the Policy Detail and Catalog view pages in `frontend/src/routes/` to correctly render the new `terms` structure.
- [ ] Task: Update the document generation logic in `frontend/src/utils/documentData.ts` to use the new text-based terms.
- [ ] Task: Write failing Playwright E2E tests in `frontend/tests/` to verify the UI changes and correct rendering of terms.
- [ ] Task: Implement UI changes to ensure tests pass.
- [ ] Task: Conductor - User Manual Verification 'Frontend UI Updates' (Protocol in workflow.md)

## Phase 4: Final Polish & Audit

- [ ] Task: Perform a comprehensive audit of all views where terms are displayed to ensure consistency.
- [ ] Task: Update any remaining documentation or help text related to policy terms.
- [ ] Task: Conductor - User Manual Verification 'Final Polish & Audit' (Protocol in workflow.md)
