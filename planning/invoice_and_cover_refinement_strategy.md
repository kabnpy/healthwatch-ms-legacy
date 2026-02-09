# Strategy: Invoice Generation & Cover Display Refinement

## Context
Currently, the system automatically aggregates all new `RiskNotes` (policies) into a single "Unpaid" invoice for a client. While convenient, this lacks flexibility when a client requires separate invoices for different policies (e.g., different cost centers or internal accounts).

Additionally, the display name for covers (specifically Motor Private) is generic (e.g., "Motor Private"), making it difficult to distinguish between multiple vehicles at a glance.

## Goals
1.  **Decouple Invoice Aggregation:** Stop automatically merging new Risk Notes into existing unpaid invoices. Each new Risk Note should generate its own distinct Invoice (or Draft Invoice) by default.
2.  **Improve Cover Visibility:** specific "Motor Private" policies should display as "Motor Private - [Registration Number]" in lists and headers.

---

## Part 1: Invoice Generation Refinement

### The Problem
The current `create_risk_note` CRUD logic searches for an existing `Invoice` with status "Unpaid" and appends the new `RiskNote` as a line item. This forces a "one invoice per client" model until payment is made.

### The Solution
Refactor the backend logic to **always create a new Invoice** for a new Risk Note.

### Implementation Plan
1.  **Backend (`backend/app/crud/insurance/policy.py`)**:
    *   Locate `create_risk_note`.
    *   Remove or comment out the logic that queries for an existing `Unpaid` invoice.
    *   Ensure a new `Invoice` is instantiated and saved for every new `RiskNote`.
    *   Ensure the `invoice_number` generation remains robust.

2.  **Verification**:
    *   Create a Risk Note -> Check Invoice List (Should see Invoice A).
    *   Create another Risk Note for same client -> Check Invoice List (Should see Invoice B).
    *   Verify `AllocationDialog` (Receipts) still lists all pending invoices correctly.

---

## Part 2: Cover Display Name Refinement

### The Problem
Users see a list of "Motor Private" policies and cannot distinguish them without clicking into details.

### The Solution
Update the UI (and potentially the backend response) to dynamically format the display name based on the policy content.

### Implementation Plan
1.  **Frontend Utility**:
    *   Create a helper function `getPolicyDisplayName(riskNote: RiskNotePublic): string`.
    *   Logic:
        *   If `class_of_insurance` (or `product_name`) is "Motor Private":
            *   Extract `reg_no` from `policy_snapshot` or `risk_details` (specifically looking in the "VEHICLE DETAILS" section).
            *   Return "Motor Private - [Reg No]".
        *   Else: Return the generic Product Name.

2.  **UI Updates**:
    *   **Policy List / Client Hub**: Update columns to use `getPolicyDisplayName`.
    *   **Coverage Card**: Update the card title.
    *   **Wizard / Headers**: Update top-level headers to reflect the specific asset.

3.  **Data Structure Analysis**:
    *   Target Data Path: `riskNote.policy_snapshot.risk_details["VEHICLE DETAILS"]["reg_no"]` (Based on codebase search).

---

## Execution Steps (Atomic)
1.  **Refactor Invoice CRUD**: Change backend logic to stop auto-merging.
2.  **Frontend Helper**: Implement `getPolicyDisplayName`.
3.  **Apply Display Name**: Update `CoverageCard`, `Policies/columns.tsx`, and `ClientInvoices`.

## Future Considerations
- **Merge Invoices**: Allow users to manually combine multiple draft/unpaid invoices into one if they *do* want a single bill.
- **Other Classes**: Extend the display name logic to Property (Plot No), Medical (Member No), etc.
