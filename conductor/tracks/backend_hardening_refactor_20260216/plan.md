# Implementation Plan: Backend Hardening & Navigation Refactor

This plan details the steps to simplify the backend architecture, harden security, and refactor the frontend navigation to be client-centric.

## Phase 1: Backend Structural Refactor & Cleanup
Flatten the backend directory structure and remove the unused `Item` module.

- [x] Task: Remove `Item` database model and generate a cleanup migration. (c104e99)
- [ ] Task: Flatten `backend/app/models/` into a simpler structure.
- [x] Task: Flatten `backend/app/schemas/` into a simpler structure. (bd500d8)
- [x] Task: Flatten `backend/app/crud/` into a simpler structure. (bd500d8)
- [x] Task: Remove `Item` CRUD logic and API routes. (bd500d8)
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Backend Structural Refactor & Cleanup' (Protocol in workflow.md)

## Phase 2: Security Hardening & Bug Fixes
Resolve the 401 Unauthorized errors and improve the testing strategy.

- [ ] Task: Audit all API endpoints for consistent `SecurityDep` usage.
- [ ] Task: Implement a centralized `MockAuth` helper for the backend test suite.
- [ ] Task: Write failing integration tests for the Policy Wizard flow (Red Phase).
- [ ] Task: Fix the 401 error in the Policy creation endpoint (Green Phase).
- [ ] Task: Verify 80%+ coverage for all modified security and policy modules.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Security Hardening & Bug Fixes' (Protocol in workflow.md)

## Phase 3: Frontend Route & Navigation Refactor
Nest the policy dashboard and remove `Item` references from the UI.

- [ ] Task: Refactor frontend routing to nest Policy views under Client routes (`/clients/$clientId/policies/$policyId`).
- [ ] Task: Update the `AppSidebar` to remove the "Items" link and improve navigation labels.
- [ ] Task: Delete all `Item` specific components, hooks, and pages.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Frontend Route & Navigation Refactor' (Protocol in workflow.md)

## Phase 4: Integration & Final Polish
Regenerate the API client and resolve discrepancies.

- [ ] Task: Regenerate the frontend API client (`npm run generate-client`).
- [ ] Task: Fix all TypeScript discrepancies across the frontend caused by backend structural changes.
- [ ] Task: Execute final build check (`npm run build`) and linting for both stack layers.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Integration & Final Polish' (Protocol in workflow.md)
