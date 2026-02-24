# Implementation Plan: Cleanup Convoluted Legacy Logic

## Phase 1: Validation & Schema Simplification
Refactor the model and schema layers to remove legacy key-mapping and nested logic.

- [ ] Task: Remove legacy schema helpers and aliases
    - [ ] Identify and remove `MotorPrivateRiskDetailsLegacy` or similar in `backend/app/schemas.py`
    - [ ] Clean up `field_validator` logic that handles legacy numeric formats or keys
- [ ] Task: Simplify `Product.validate_risk_details`
    - [ ] Remove `key_mapping` dictionary and loops in `backend/app/models.py`
    - [ ] Remove nested "VEHICLE DETAILS" extraction logic
    - [ ] Implement direct Pydantic validation using the new flat structure
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Validation & Schema Simplification' (Protocol in workflow.md)

## Phase 2: Service Layer Refactoring
Clean up the Policy and RiskNote services to remove snapshot dependencies and redundant logic.

- [ ] Task: Write failing tests for simplified Policy Service
    - [ ] Create tests that validate policy creation using ONLY flat `risk_details`
    - [ ] Create tests for endorsements verifying delta-only change logs
- [ ] Task: Refactor `create_policy` in `PolicyService`
    - [ ] Remove `policy_snapshot` assignment logic
    - [ ] Ensure `risk_details` are passed directly from validated output
- [ ] Task: Refactor `create_endorsement` in `PolicyService`
    - [ ] Remove snapshot retrieval and comparison logic
    - [ ] Ensure the delta calculation uses the singular semantic state on the Policy object
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Service Layer Refactoring' (Protocol in workflow.md)

## Phase 3: Rating Engine Cleanup
Standardize the rating strategies to use the authoritative `sum_insured` key.

- [ ] Task: Write failing tests for Rating Engine standardization
    - [ ] Verify `RatingService` fails if provided with nested or legacy keys
- [ ] Task: Simplify `RatingService._calculate_generic`
    - [ ] Remove the fallback logic for searching `financials` or nested `sum_insured`
- [ ] Task: Standardize `MotorPrivateRatingStrategy`
    - [ ] Ensure it pulls `sum_insured` directly from the risk details dictionary
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Rating Engine Cleanup' (Protocol in workflow.md)

## Phase 4: Migration & Database Finalization
Ensure the database schema and migration history are clean and strictly follow the new models.

- [ ] Task: Review and cleanup recent migration versions
    - [ ] Ensure the latest migrations don't contain "best-effort" data loss risks for clean system deployment
- [ ] Task: Final System Verification
    - [ ] Run E2E Playwright tests to ensure wizard flows still work with the simplified backend
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Migration & Database Finalization' (Protocol in workflow.md)
