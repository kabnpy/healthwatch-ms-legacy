# Implementation Plan: Remove Endorsement Workflow

## Phase 0: Preparation & Branching
- [ ] Task: Create a new git branch for this track.
    - [ ] Run `git checkout -b feature/remove-endorsement-workflow`.
    - [ ] Stage and commit any existing/pending changes to ensure a clean slate.
- [ ] Task: Confirm the environment is stable before starting.
    - [ ] Run all existing tests to ensure they pass.

## Phase 1: Backend Cleanup
- [ ] Task: Identify and map all Endorsement-related code in the backend.
    - [ ] List all API routes in `backend/app/api/` that mention "Endorsement".
    - [ ] List all methods in `backend/app/services/` (especially `PolicyService`) related to endorsements.
    - [ ] Find all database models or schemas (e.g., `backend/app/models.py`, `backend/app/schemas.py`) with endorsement fields.
- [ ] Task: Write Failing Tests (Red Phase) to verify the removal of Endorsement functionality.
    - [ ] Create a test that expects a 404 for removed endorsement endpoints.
    - [ ] Create a test ensuring that only "New Business" and "Renewal" types remain valid for `RiskNote` snapshots.
- [ ] Task: Remove Endorsement logic and models from the backend.
    - [ ] Delete or refactor API endpoints.
    - [ ] Clean up service layer logic.
    - [ ] Remove fields from `SQLModel` and `Pydantic` schemas.
    - [ ] Update any database migration scripts (Alembic) if models were changed.
- [ ] Task: Implement to Pass Tests (Green Phase).
    - [ ] Confirm all backend tests pass, including the new failure expectations.
- [ ] Task: Conductor - User Manual Verification 'Backend Cleanup' (Protocol in workflow.md)

## Phase 2: Frontend Cleanup
- [ ] Task: Identify and map all Endorsement-related components in the frontend.
    - [ ] Find all occurrences of "Endorse" or "Endorsement" in `frontend/src/`.
    - [ ] Identify UI buttons, links, and forms specific to endorsements.
- [ ] Task: Write Failing Tests (Red Phase) for frontend removal.
    - [ ] Add Playwright tests that fail to find "Endorsement" UI elements.
- [ ] Task: Remove Endorsement UI elements and logic.
    - [ ] Remove buttons from the Policy Detail page.
    - [ ] Remove any specific endorsement forms or logic from TanStack Router/Query hooks.
- [ ] Task: Implement to Pass Tests (Green Phase).
    - [ ] Verify frontend build and run E2E tests to ensure "Endorse" is gone and core flows still work.
- [ ] Task: Conductor - User Manual Verification 'Frontend Cleanup' (Protocol in workflow.md)

## Phase 3: Final Verification & Stability
- [ ] Task: Run full regression test suite (Backend and Frontend).
    - [ ] Verify that creating a new `RiskNote` for "New Business" and "Renewal" still works perfectly.
- [ ] Task: Commit all changes and merge if requested.
    - [ ] Finalize the branch and prepare for merge.
- [ ] Task: Conductor - User Manual Verification 'Final Verification & Stability' (Protocol in workflow.md)
