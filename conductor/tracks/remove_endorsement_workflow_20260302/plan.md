# Implementation Plan: Remove Endorsement Workflow

## Phase 0: Preparation & Branching
- [x] Task: Create a new git branch for this track. [9823f0f]
    - [x] Run `git checkout -b feature/remove-endorsement-workflow`.
    - [x] Stage and commit any existing/pending changes to ensure a clean slate.
- [x] Task: Confirm the environment is stable before starting. [9823f0f]
    - [x] Run all existing tests to ensure they pass.

## Phase 1: Backend Cleanup
- [x] Task: Identify and map all Endorsement-related code in the backend. [9823f0f]
    - [x] List all API routes in `backend/app/api/` that mention "Endorsement".
    - [x] List all methods in `backend/app/services/` (especially `PolicyService`) related to endorsements.
    - [x] Find all database models or schemas (e.g., `backend/app/models.py`, `backend/app/schemas.py`) with endorsement fields.
- [x] Task: Write Failing Tests (Red Phase) to verify the removal of Endorsement functionality. [9823f0f]
    - [x] Create a test that expects a 404 for removed endorsement endpoints.
    - [x] Create a test ensuring that only "New Business" and "Renewal" types remain valid for `RiskNote` snapshots.
- [x] Task: Remove Endorsement logic and models from the backend. [9823f0f]
    - [x] Delete or refactor API endpoints.
    - [x] Clean up service layer logic.
    - [x] Remove fields from `SQLModel` and `Pydantic` schemas.
    - [x] Update any database migration scripts (Alembic) if models were changed.
- [x] Task: Implement to Pass Tests (Green Phase). [9823f0f]
    - [x] Confirm all backend tests pass, including the new failure expectations.
- [ ] Task: Conductor - User Manual Verification 'Backend Cleanup' (Protocol in workflow.md)

## Phase 2: Frontend Cleanup
- [x] Task: Identify and map all Endorsement-related components in the frontend. [9823f0f]
    - [x] Find all occurrences of "Endorse" or "Endorsement" in `frontend/src/`.
    - [x] Identify UI buttons, links, and forms specific to endorsements.
- [x] Task: Write Failing Tests (Red Phase) for frontend removal. [9823f0f]
    - [x] Add Playwright tests that fail to find "Endorsement" UI elements.
- [x] Task: Remove Endorsement UI elements and logic. [9823f0f]
    - [x] Remove buttons from the Policy Detail page.
    - [x] Remove any specific endorsement forms or logic from TanStack Router/Query hooks.
- [x] Task: Implement to Pass Tests (Green Phase). [9823f0f]
    - [x] Verify frontend build and run E2E tests to ensure "Endorse" is gone and core flows still work.
- [ ] Task: Conductor - User Manual Verification 'Frontend Cleanup' (Protocol in workflow.md)

## Phase 3: Final Verification & Stability
- [x] Task: Run full regression test suite (Backend and Frontend). [9823f0f]
    - [x] Verify that creating a new `RiskNote` for "New Business" and "Renewal" still works perfectly.
- [x] Task: Commit all changes and merge if requested. [9823f0f]
    - [x] Finalize the branch and prepare for merge.
- [ ] Task: Conductor - User Manual Verification 'Final Verification & Stability' (Protocol in workflow.md)

## Phase: Review Fixes
- [x] Task: Apply review suggestions 9884309

