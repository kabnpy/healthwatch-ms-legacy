# Implementation Plan: Backend Model Streamlining & Debt Reduction

## Phase 1: Core Model Refactor [checkpoint: 5940fb6]
Refactor the primary models to centralize risk data and eliminate redundancy.

- [x] **Task: Update `Policy` Model for Authoritative State** [e49be45]
    - [x] Update `backend/app/models.py`: Add `risk_details: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))` to the `Policy` model.
    - [x] Remove computed properties on `Policy` that perform relationship traversals (`current_risk_details`, `total_premium`, `start_date`, `end_date`, `display_name`).
- [x] **Task: Refactor `RiskNote` and Remove Redundant Fields** [e49be45]
    - [x] Update `backend/app/models.py`: Remove `policy_snapshot` and `payment_status` from `RiskNote`.
    - [x] Ensure `RiskNote` has `change_log: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))` for recording diffs.
- [x] **Task: Standardize Project Enums** [e49be45]
    - [x] Align `PolicyStatus`, `TransactionType`, and other enums with the streamlined definitions in `planning/models.py`.
- [ ] **Task: Conductor - User Manual Verification 'Core Model Refactor' (Protocol in workflow.md)**

## Phase 2: Data Migration & Integration [checkpoint: c9ddd37]
Safely migrate existing data and update service logic to the new structure.

- [x] **Task: Create and Verify Alembic Migration** [c9ddd37]
    - [x] Generate a migration to add `Policy.risk_details` and remove old columns.
    - [x] **CRITICAL:** Include an `upgrade()` script that populates `Policy.risk_details` from the *most recent* `RiskNote.policy_snapshot` for each policy.
- [x] **Task: Update `PolicyService` and `CRUD` Logic** [c9ddd37]
    - [x] Update `backend/app/crud.py` to handle `risk_details` on the `Policy` model during creation and updates.
    - [x] Refactor endorsement logic to update `Policy.risk_details` in-place and record the diff in `RiskNote.change_log`.
- [x] **Task: Update Financial Status Logic** [c9ddd37]
    - [x] Refactor any logic that checked `RiskNote.payment_status` to instead derive it from the linked `Invoice.balance_due`.
- [x] **Task: Conductor - User Manual Verification 'Data Migration & Integration' (Protocol in workflow.md)**

## Phase 3: Validation & Cleanup [checkpoint: d72c2a6]
Ensure full system integrity and remove any remaining technical debt.

- [x] **Task: Update Backend Test Suite** [d72c2a6]
    - [x] Refactor existing tests in `backend/tests/` that relied on the old model structure (especially `test_soft_delete.py`, `test_transactional_models.py`).
    - [x] Ensure tests verify the "single source of truth" for risk data and derived payment status.
- [x] **Task: Verify Coverage & Performance** [d72c2a6]
    - [x] Run coverage reports and ensure >80% coverage for the refactored models and services.
    - [x] Monitor for any "n+1" query issues introduced by the refactor.
- [x] **Task: Conductor - User Manual Verification 'Validation & Cleanup' (Protocol in workflow.md)**

## Phase: Review Fixes
- [~] Task: Apply review suggestions
