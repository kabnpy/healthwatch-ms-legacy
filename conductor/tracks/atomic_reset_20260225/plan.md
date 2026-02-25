# Implementation Plan: Atomic Reset (Structural Simplification)

This plan implements the "Atomic Snapshot" architecture, simplifying the Policy/RiskNote relationship and moving document terms to text-based fields.

## Phase 1: Database & Model Refactoring
Focus: Strip Policy metadata and enhance RiskNote for full snapshots.

- [ ] Task: Write tests for new `Policy`, `RiskNote`, and `Product` model structures.
- [ ] Task: Update `backend/app/models.py` to remove `risk_details` from `Policy` and enhance `RiskNote`.
- [ ] Task: Create and apply a "Clean Slate" Alembic migration for the new schema.
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Service Layer & Business Logic
Focus: Implement atomic creation/endorsement and text-based terms logic.

- [ ] Task: Write tests for `PolicyService` atomic snapshot creation and endorsement.
- [ ] Task: Refactor `backend/app/services/policy.py` to remove diffing logic and use full snapshots.
- [ ] Task: Update `RatingService` to handle the revised `cover_snapshot` structure.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: API & Public Schemas
Focus: Expose the "Current State" (active note) via the Policy API.

- [ ] Task: Write tests for `PolicyPublic` schema with the `active_note` field.
- [ ] Task: Update `backend/app/schemas.py` and API utilities to populate `active_note`.
- [ ] Task: Verify `/policies/{id}` endpoint returns the correct atomic snapshot.
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Frontend UI & Experience
Focus: Align the UI wizard and history view with the new atomic model.

- [ ] Task: Update Frontend TypeScript types and regenerate the API client.
- [ ] Task: Refactor the New Policy Wizard to support text-based Terms and the new snapshot structure.
- [ ] Task: Implement the "Version History" view on the Policy detail page.
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)
