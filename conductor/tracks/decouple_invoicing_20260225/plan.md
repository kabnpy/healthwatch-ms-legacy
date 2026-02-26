# Implementation Plan: Decouple Risk Note and Invoice Creation

## Phase 1: Backend Service Refactoring (Decoupling)
- [x] Task: Write tests for `PolicyService` to verify Risk Note creation without Invoices. 55aebe2
- [ ] Task: Refactor `PolicyService.create_policy` and `create_endorsement` to remove automatic invoice generation.
- [ ] Task: Rename `create_risk_note_with_invoice` to `create_risk_note` and remove internal invoice creation logic.
- [ ] Task: Conductor - User Manual Verification 'Backend Decoupling' (Protocol in workflow.md)

## Phase 2: Data Model & Authoritative Link
- [ ] Task: Create a database migration to remove/deprecate the `invoice_number` field from the `risknote` table.
- [ ] Task: Update the `RiskNote` SQLModel to remove the `invoice_number` field.
- [ ] Task: Implement a backend utility or service method to fetch "un-invoiced" Risk Notes (filtering by those without `InvoiceLineItem`).
- [ ] Task: Write tests for the "un-invoiced" detection logic.
- [ ] Task: Conductor - User Manual Verification 'Data Model & Linking' (Protocol in workflow.md)

## Phase 3: Frontend & Wizard Integration
- [ ] Task: Update the `InvoiceWizard` component to fetch and display only un-invoiced Risk Notes.
- [ ] Task: Update the Risk Note detail view to retrieve the associated Invoice via the `invoice_line_items` relationship instead of `invoice_number`.
- [ ] Task: Verify consolidated invoice generation works correctly with the refactored backend logic.
- [ ] Task: Conductor - User Manual Verification 'Frontend Integration' (Protocol in workflow.md)
