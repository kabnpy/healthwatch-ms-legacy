# Implementation Plan: Centralized Rating Engine & Financial Hardening

This plan details the centralization of insurance rating logic into a backend service, the implementation of polymorphic financial snapshots, and the real-time integration with the frontend wizard.

## Phase 1: Rating Engine & Polymorphic Schemas [checkpoint: 2f35acd]
Establish the core logic and validation models for financial breakdowns.

- [x] Task: Create a new feature branch `feat/rating-engine`. (manual)
- [x] Task: **Write Tests for Financial Schemas**: Define expected structures for `BaseFinancialBreakdown` and `MotorFinancialBreakdown`. (Red Phase Complete)
- [x] Task: Implement polymorphic Pydantic schemas in `backend/app/schemas.py` using `Annotated` and `Discriminator`. (30bc787)
- [x] Task: **Write Tests for Rating Service**: Define test cases for Motor Private math (PVT, Excess Protector, etc.) with `Decimal` precision. (Red Phase Complete)
- [x] Task: Implement `RatingService` and `MotorPrivateRatingStrategy` in `backend/app/services/rating.py` using the Strategy Pattern. (9f7d7cb)
- [x] Task: Conductor - User Manual Verification 'Phase 1: Rating Engine & Polymorphic Schemas' (Protocol in workflow.md) (2f35acd)

## Phase 2: Persistence Layer & Migration [checkpoint: 0a668f7]
Update the database schema to store authoritative financial snapshots.

- [x] Task: Update `RiskNote` model in `backend/app/models.py` to rename `taxes` to `financial_breakdown` and update types. (ebaebc1)
- [x] Task: Generate and verify an Alembic migration for the column rename and data transformation. (05af0e7)
- [x] Task: Update `crud.py` and `PolicyService` to support the new `financial_breakdown` structure. (1334e77)
- [x] Task: **Write Integration Tests**: Verify that creating a policy correctly persists the full financial breakdown. (1334e77)
- [x] Task: Conductor - User Manual Verification 'Phase 2: Persistence Layer & Migration' (Protocol in workflow.md) (0a668f7)

## Phase 3: Quote API & Service Orchestration [checkpoint: 69a0e0b]
Expose the rating engine via API and integrate it into the policy issuance flow.

- [x] Task: Implement `POST /api/v1/policies/quote` endpoint in `backend/app/api/routes/policies.py`. (f1293a1)
- [x] Task: Refactor `PolicyService.create_policy` to call `RatingService` as the source of truth before saving. (f1293a1)
- [x] Task: **Verify Coverage**: Ensure >80% coverage for the new rating and quote logic. (f1293a1)
- [x] Task: Conductor - User Manual Verification 'Phase 3: Quote API & Service Orchestration' (Protocol in workflow.md) (69a0e0b)

## Phase 4: Frontend Integration & Single Source of Truth [checkpoint: 57552e5]
Connect the wizard to the authoritative backend math and remove duplicated logic.

- [x] Task: Remove `frontend/src/lib/calculator.ts` and all local math references. (57552e5)
- [x] Task: Update `StepFinancials.tsx` to handle loading/error states for the authoritative quote. (57552e5)
- [x] Task: Ensure `StepReview.tsx` and `RiskNoteTemplate.tsx` use the `financial_breakdown` from the backend exclusively. (57552e5)
- [x] Task: Regenerate frontend API client to ensure all new schema fields are available. (52554f6)
- [x] Task: Conductor - User Manual Verification 'Phase 4: Single Source of Truth' (Protocol in workflow.md) (57552e5)
