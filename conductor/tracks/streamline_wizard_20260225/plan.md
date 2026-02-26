# Implementation Plan: Streamline New Policy Wizard

## Phase 1: Identity & Structure Refactor
*   **Goal:** Consolidate product selection and introduce the manual policy number field.
*   - [x] Task: Update `NewPolicyWizard` state type to include a mandatory `policyNumber` field. d1dc73a
*   - [x] Task: Refactor `StepAsset` (Step 1) to include the "Policy Number" input field with professional copy.
*   - [x] Task: Update wizard navigation logic to skip the "Terms" step entirely.
*   - [ ] Task: Conductor - User Manual Verification 'Identity & Structure' (Protocol in workflow.md)

## Phase 2: Core Data Simplification
*   **Goal:** Streamline the risk detail and financial capture steps.
*   - [ ] Task: Update `StepBlueprint` (Step 2) to display only Registration Number, Make, and Year of Manufacture.
*   - [ ] Task: Update `StepFinancials` (Step 3) to focus on Sum Insured and Period of Cover.
*   - [ ] Task: Remove `StepTerms` component and all references to it within the wizard.
*   - [ ] Task: Conductor - User Manual Verification 'Core Data Simplification' (Protocol in workflow.md)

## Phase 3: Submission & Copy Overhaul
*   **Goal:** Finalize submission logic and apply professional tone across the wizard.
*   - [ ] Task: Update `handleIssuePolicy` in `NewPolicyWizard` to correctly map the custom `policyNumber` to the backend request.
*   - [ ] Task: Refactor `StepReview` to show a clean summary of the simplified data.
*   - [ ] Task: Perform a comprehensive copy audit and update all wizard labels/placeholders to "Professional & Minimal" tone.
*   - [ ] Task: Conductor - User Manual Verification 'Submission & Polish' (Protocol in workflow.md)
