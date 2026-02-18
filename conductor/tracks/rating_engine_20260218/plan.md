# Implementation Plan: Centralized Rating Engine & Financial Hardening

This plan details the centralization of insurance rating logic into a backend service, the implementation of polymorphic financial snapshots, and the real-time integration with the frontend wizard.

## Phase 1: Rating Engine & Polymorphic Schemas [checkpoint: ]
Establish the core logic and validation models for financial breakdowns.

- [ ] Task: Create a new feature branch `feat/rating-engine`.
- [ ] Task: **Write Tests for Financial Schemas**: Define expected structures for `BaseFinancialBreakdown` and `MotorFinancialBreakdown`.
- [ ] Task: Implement polymorphic Pydantic schemas in `backend/app/schemas.py` using `Annotated` and `Discriminator`.
- [ ] Task: **Write Tests for Rating Service**: Define test cases for Motor Private math (PVT, Excess Protector, etc.) with `Decimal` precision.
- [ ] Task: Implement `RatingService` and `MotorPrivateRatingStrategy` in `backend/app/services/rating.py` using the Strategy Pattern.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Rating Engine & Polymorphic Schemas' (Protocol in workflow.md)

## Phase 2: Persistence Layer & Migration [checkpoint: ]
Update the database schema to store authoritative financial snapshots.

- [ ] Task: Update `RiskNote` model in `backend/app/models.py` to rename `taxes` to `financial_breakdown` and update types.
- [ ] Task: Generate and verify an Alembic migration for the column rename and data transformation.
- [ ] Task: Update `crud.py` and `PolicyService` to support the new `financial_breakdown` structure.
- [ ] Task: **Write Integration Tests**: Verify that creating a policy correctly persists the full financial breakdown.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Persistence Layer & Migration' (Protocol in workflow.md)

## Phase 3: Quote API & Service Orchestration [checkpoint: ]
Expose the rating engine via API and integrate it into the policy issuance flow.

- [ ] Task: Implement `POST /api/v1/policies/quote` endpoint in `backend/app/api/routes/policies.py`.
- [ ] Task: Refactor `PolicyService.create_policy` to call `RatingService` as the source of truth before saving.
- [ ] Task: **Verify Coverage**: Ensure >80% coverage for the new rating and quote logic.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Quote API & Service Orchestration' (Protocol in workflow.md)

## Phase 4: Frontend Integration & Real-time UI [checkpoint: ]
Connect the wizard to the authoritative backend math.

- [ ] Task: Regenerate frontend API client (`npm run generate-client`).
- [ ] Task: Implement a debounced `useQuote` hook in `frontend/src/hooks/useInsurance.ts`.
- [ ] Task: Refactor `StepFinancials.tsx` in the New Policy Wizard to display backend-calculated prices.
- [ ] Task: Update the `RiskNoteTemplate.tsx` and Review step to render the detailed breakdown from `financial_breakdown`.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Frontend Integration & Real-time UI' (Protocol in workflow.md)
