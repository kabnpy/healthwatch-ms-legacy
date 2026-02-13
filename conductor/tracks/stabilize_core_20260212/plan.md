# Implementation Plan: Stabilize and Refine Core Functionality

This plan outlines the steps to stabilize and polish the HealthWatch MS core functionality.

## Phase 1: Type Stabilization & Build Integrity
- [x] Task: Audit and Resolve Critical Frontend TypeScript Errors (14c0dad)
    - [x] Resolve errors in auto-generated client types.
    - [x] Fix type mismatches in `frontend/src/types/insurance.ts` and related components.
    - [x] Ensure `npm run build` passes in the frontend.
- [x] Task: Backend Schema and Migration Verification (verified)
    - [x] Verify `risk_note_number` migration is consistent with the latest models.
    - [x] Run backend tests to ensure 1:1 Policy/RiskItem refactor is stable.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Type Stabilization' (Protocol in workflow.md)

## Phase 2: UI/UX Refinement & Polish
- [ ] Task: Implement Refined Empty States & Skeletons
    - [ ] Update `Client Hub` empty states to be contextual and instructive.
    - [ ] Add/Refine skeleton loaders for the Insurance Dashboard tabs.
- [ ] Task: Aesthetic Standardization
    - [ ] Audit UI for adherence to "Subtle Neutrals" palette.
    - [ ] Ensure "Visual Clarity" (whitespace) is consistent across all main views.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: UI/UX Refinement' (Protocol in workflow.md)

## Phase 3: Workflow Hardening & Final Verification
- [ ] Task: Harden Core Insurance Flows
    - [ ] Verify "New Business" wizard end-to-end with various inputs.
    - [ ] Ensure Risk Note/Debit Note generation is robust and correctly formatted.
- [ ] Task: Final Quality Audit
    - [ ] Run full test suite (Pytest & Playwright).
    - [ ] Execute final linting check (`ruff` and `biome`).
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Workflow Hardening' (Protocol in workflow.md)
