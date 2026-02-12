# Specification: Stabilize and Refine Core Functionality

## 1. Overview
This track focuses on transforming the current codebase into a production-ready, shippable product. The primary objectives are resolving technical debt (TypeScript errors), polishing the user experience, and ensuring the reliability of the core insurance workflows.

## 2. Objectives
- **Type Integrity:** Resolve persistent TypeScript errors in the frontend, particularly those related to the auto-generated client and complex insurance types.
- **UI/UX Polish:** Refine empty states, loading indicators (skeletons), and ensure consistent adherence to the "Subtle Neutrals" and "Visual Clarity" design principles.
- **Workflow Hardening:** Verify and fix edge cases in the New Business and Risk Note generation flows.
- **Production Readiness:** Ensure all linting and type-checking passes without errors.

## 3. Scope
- **Frontend Components:** Review and fix types in `ClientInvoices.tsx`, `DocumentViewer.tsx`, and the Wizard components.
- **Insurance Models:** Ensure the backend `SQLModel` changes are correctly reflected in the frontend types.
- **Calculators:** Verify the accuracy and stability of the Motor Private premium calculations.

## 4. Success Criteria
- Zero high-priority TypeScript errors in the `frontend` build.
- UI follows the "Papermark" aesthetic with refined empty states and skeletons.
- All core workflows (Client -> Policy -> Risk Note) are verified and stable.
