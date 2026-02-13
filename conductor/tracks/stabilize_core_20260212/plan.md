# Implementation Plan: Stabilize and Refine Core Functionality

This plan outlines the steps to stabilize and polish the HealthWatch MS core functionality.

## Phase 1: Type Stabilization & Build Integrity [checkpoint: cf0192d]
- [x] Task: Audit and Resolve Critical Frontend TypeScript Errors (14c0dad)
    - [x] Resolve errors in auto-generated client types.
    - [x] Fix type mismatches in `frontend/src/types/insurance.ts` and related components.
    - [x] Ensure `npm run build` passes in the frontend.
- [x] Task: Backend Schema and Migration Verification (verified)
    - [x] Verify `risk_note_number` migration is consistent with the latest models.
    - [x] Run backend tests to ensure 1:1 Policy/RiskItem refactor is stable.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Type Stabilization' (cf0192d)

## Phase 2: UI/UX Refinement & Polish [checkpoint: 61888cc]
- [x] Task: Implement Refined Empty States & Skeletons (61888cc)
    - [x] Update `Client Hub` empty states to be contextual and instructive.
    - [x] Add/Refine skeleton loaders for the Insurance Dashboard tabs.
- [x] Task: Aesthetic Standardization (verified)
    - [x] Audit UI for adherence to "Subtle Neutrals" palette.
    - [x] Ensure "Visual Clarity" (whitespace) is consistent across all main views.
- [x] Task: Conductor - User Manual Verification 'Phase 2: UI/UX Refinement' (61888cc)

## Phase 3: Workflow Hardening & Final Verification
- [x] Task: Harden Core Insurance Flows (verified)
    - [x] Verify "New Business" wizard end-to-end with various inputs.
    - [x] Ensure Risk Note/Debit Note generation is robust and correctly formatted.
- [x] Task: Final Quality Audit (verified)
    - [x] Run full test suite (Pytest & Playwright).
    - [x] Execute final linting check (`ruff` and `biome`).
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Workflow Hardening' (Protocol in workflow.md)
