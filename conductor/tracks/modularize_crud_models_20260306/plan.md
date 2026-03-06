# Implementation Plan: Refactor CRUD and Models into Modules

This plan follows the modularization strategy for `backend/app/models.py` and `backend/app/crud.py` into domain-specific modules with unified exports.

## Phase 0: Setup and Branching
- [x] Task: Create a new git branch for the refactoring: `git checkout -b refactor/modularize-crud-models`. f7b7654
- [ ] Task: Conductor - User Manual Verification 'Phase 0: Setup and Branching' (Protocol in workflow.md)

## Phase 1: Models Modularization
- [ ] Task: Create `backend/app/models/` directory and `__init__.py`.
- [ ] Task: Create `backend/app/models/audit.py` and move shared audit fields/base models.
- [ ] Task: Create `backend/app/models/user.py` and move Auth/User/Item models.
- [ ] Task: Create `backend/app/models/client.py` and move Client-related models.
- [ ] Task: Create `backend/app/models/policy.py` and move Policy/RiskNote/Finance models.
- [ ] Task: Create `backend/app/models/claim.py` and move Claim models.
- [ ] Task: Update `backend/app/models/__init__.py` with unified exports.
- [ ] Task: Verify models refactor with existing tests.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Models Modularization' (Protocol in workflow.md)

## Phase 2: CRUD Modularization
- [ ] Task: Create `backend/app/crud/` directory and `__init__.py`.
- [ ] Task: Create `backend/app/crud/user.py` and move User/Auth CRUD logic.
- [ ] Task: Create `backend/app/crud/client.py` and move Client CRUD logic.
- [ ] Task: Create `backend/app/crud/policy.py` and move Policy/RiskNote CRUD logic.
- [ ] Task: Create `backend/app/crud/claim.py` and move Claim CRUD logic.
- [ ] Task: Update `backend/app/crud/__init__.py` with unified exports.
- [ ] Task: Verify CRUD refactor with existing tests.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: CRUD Modularization' (Protocol in workflow.md)

## Phase 3: Cleanup and Final Integration
- [ ] Task: Update all import sites in `backend/app/api/`, `backend/app/core/`, and `backend/app/tests/` to use the new modular structure where direct imports are used.
- [ ] Task: Remove or empty the original `backend/app/models.py` and `backend/app/crud.py`.
- [ ] Task: Run full backend test suite to ensure no regressions or circular dependencies.
- [ ] Task: Run linting and type checking (mypy, ruff).
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Cleanup and Final Integration' (Protocol in workflow.md)
