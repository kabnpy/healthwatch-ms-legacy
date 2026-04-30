# Implementation Plan: Refactor CRUD and Models into Modules

This plan follows the modularization strategy for `backend/app/models.py` and `backend/app/crud.py` into domain-specific modules with unified exports.

## Phase 0: Setup and Branching [checkpoint: 842a023]
- [x] Task: Create a new git branch for the refactoring: `git checkout -b refactor/modularize-crud-models`. f7b7654
- [x] Task: Conductor - User Manual Verification 'Phase 0: Setup and Branching' (Protocol in workflow.md)

## Phase 1: Models Modularization [checkpoint: 814e63c]
- [x] Task: Create `backend/app/models/` directory and `__init__.py`. f7b7654
- [x] Task: Create `backend/app/models/audit.py` and move shared audit fields/base models. f7b7654
- [x] Task: Create `backend/app/models/user.py` and move Auth/User/Item models. f7b7654
- [x] Task: Create `backend/app/models/client.py` and move Client-related models. f7b7654
- [x] Task: Create `backend/app/models/policy.py` and move Policy/RiskNote/Finance models. f7b7654
- [x] Task: Create `backend/app/models/claim.py` and move Claim models. f7b7654
- [x] Task: Update `backend/app/models/__init__.py` with unified exports. f7b7654
- [x] Task: Verify models refactor with existing tests. f7b7654
- [x] Task: Conductor - User Manual Verification 'Phase 1: Models Modularization' (Protocol in workflow.md)

## Phase 2: CRUD Modularization [checkpoint: 373961b]
- [x] Task: Create `backend/app/crud/` directory and `__init__.py`. f7b7654
- [x] Task: Create `backend/app/crud/user.py` and move User/Auth CRUD logic. f7b7654
- [x] Task: Create `backend/app/crud/client.py` and move Client CRUD logic. f7b7654
- [x] Task: Create `backend/app/crud/policy.py` and move Policy/RiskNote CRUD logic. f7b7654
- [x] Task: Create `backend/app/crud/claim.py` and move Claim CRUD logic. f7b7654
- [x] Task: Update `backend/app/crud/__init__.py` with unified exports. f7b7654
- [x] Task: Verify CRUD refactor with existing tests. f7b7654
- [x] Task: Conductor - User Manual Verification 'Phase 2: CRUD Modularization' (Protocol in workflow.md)

## Phase 3: Cleanup and Final Integration [checkpoint: 4beb1c0]
- [x] Task: Update all import sites in `backend/app/api/`, `backend/app/core/`, and `backend/app/tests/` to use the new modular structure where direct imports are used. f7b7654
- [x] Task: Remove or empty the original `backend/app/models.py` and `backend/app/crud.py`. f7b7654
- [x] Task: Run full backend test suite to ensure no regressions or circular dependencies. f7b7654
- [x] Task: Run linting and type checking (mypy, ruff). f7b7654
- [x] Task: Conductor - User Manual Verification 'Phase 3: Cleanup and Final Integration' (Protocol in workflow.md)
