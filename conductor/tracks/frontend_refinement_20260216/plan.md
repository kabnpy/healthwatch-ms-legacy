# Implementation Plan: Frontend Aesthetic & Copy Refinement

This plan details the steps to transition the HealthWatch MS interface to a "Modern and Minimal" identity, focusing on typography, whitespace, and structural consistency.

## Phase 1: Identity & Layout Foundation
Establish the new design language and core structural changes.

- [x] Task: Update `conductor/product-guidelines.md` to codify "Modern and Minimal" principles. (586b8ff)
- [x] Task: Refactor `frontend/src/components/Common/AppSidebar.tsx` to use the `inset` variant. (23829a0)
- [ ] Task: Update main layout containers to remove 3-column constraints and implement a clean, single-content area.
- [ ] Task: Implement a global `Breadcrumbs` component to support layered navigation.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Identity & Layout Foundation' (Protocol in workflow.md)

## Phase 2: Professional Document Redesign
Standardize and polish the output templates for Risk Notes and Invoices.

- [ ] Task: Redesign `frontend/src/components/Documents/templates/RiskNoteTemplate.tsx` using a professional grid-based layout.
- [ ] Task: Redesign `frontend/src/components/Documents/templates/InvoiceTemplate.tsx` to align with the Risk Note aesthetic.
- [ ] Task: Audit and standardize border, divider, and typography styles across all document templates.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Professional Document Redesign' (Protocol in workflow.md)

## Phase 3: Component & Copy Audit
Enforce visual consistency and refine interface communication.

- [ ] Task: Audit and update action labels (buttons/links) in `NewBusinessWizard` and `EndorsementFlow`.
- [ ] Task: Refine feedback messages and toasts for a "Direct & Clear" tone across all modules.
- [ ] Task: Audit Shadcn/UI component usage (Cards, Tables, Dialogs) for consistent background and border treatments.
- [ ] Task: Standardize spacing and typographic hierarchy in the `Client Hub` and `Insurance Dashboard`.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Component & Copy Audit' (Protocol in workflow.md)

## Phase 4: Final Verification & Quality Gate
Ensure the entire system adheres to the new standards without regressions.

- [ ] Task: Run full Playwright E2E test suite to ensure no layout regressions in critical flows.
- [ ] Task: Execute final build check (`npm run build`) and linting (`biome check`).
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Final Verification & Quality Gate' (Protocol in workflow.md)
