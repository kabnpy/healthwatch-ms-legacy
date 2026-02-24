# Specification: Cleanup Convoluted Legacy Logic

## Overview
This track focuses on removing technical debt introduced during the transition to streamlined models. The system has accumulated workarounds and "best-effort" mapping logic to maintain backwards compatibility, which is no longer required. We will strictly enforce the "Single Source of Truth" principle by making the service and validation layers work directly with the new schema without fallbacks.

## Functional Requirements
- **Validation Cleanup:** Remove all nested data checks and legacy key mapping (e.g., mapping "Value Kshs." to "sum_insured") in the Pydantic schemas and `validate_risk_details` methods.
- **Policy Service Refactor:** 
    - Remove all references to `policy_snapshot` in `PolicyService`.
    - Ensure `create_policy` and `create_endorsement` logic works exclusively with the `risk_details` stored on the `Policy` object and the `change_log` deltas.
- **Rating Engine Standardization:** 
    - Clean up the `RatingService` fallback logic that searches for financials in nested objects.
    - Standardize the `MotorPrivateRatingStrategy` to use top-level semantic keys exclusively.
- **Migration Hardening:** Review the latest Alembic migrations to remove any "best-effort" data transformation logic that isn't strictly necessary for a clean system.

## Non-Functional Requirements
- **Single Source of Truth:** Authoritative data must live on the primary model (e.g., `Policy.risk_details`), not in redundant snapshots.
- **Code Clarity:** Significant reduction in logic complexity in the Service and Model layers.
- **Data Integrity:** All financial calculations must maintain decimal precision without using legacy "float" conversions except for final JSON serialization.

## Acceptance Criteria
- [ ] `MotorPrivateRiskDetails` schema has no legacy aliases or validators for old keys.
- [ ] `Product.validate_risk_details` method is simplified to direct validation without key-mapping loops.
- [ ] `PolicyService` implementation has no `policy_snapshot` assignments or retrievals.
- [ ] `RatingService` logic only pulls from standardized top-level keys.
- [ ] All unit and integration tests pass using only the new flat data structures.

## Out of Scope
- Adding new insurance classes.
- Modifying the UI components (except where needed to align with schema changes).
