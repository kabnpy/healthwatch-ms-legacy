# Strategy: Policy Wizard Value Sync

## Goal
Ensure that the "Value" (or similar field) entered in Step 1 (Details/Blueprint) of the New Policy Wizard is automatically carried over to the "Sum Insured" field in Step 2 (Financials) for products where premium is percentage-based (e.g., Motor).

## 1. Analysis
- **Current State**:
    - **Step 1 (Details)**: Uses `StepBlueprint.tsx` to render dynamic fields based on `product.product_details`. For Motor products, this usually includes a "Value" or "Value Kshs." field.
    - **Step 2 (Financials)**: Uses `StepFinancials.tsx` which has a separate `sumInsured` field in its local state/form.
    - **State Management**: `NewPolicyWizard.tsx` holds the master state (`state.details` and `state.financials`).
- **Problem**: The user enters the vehicle value in Step 1, but then has to re-enter it as "Sum Insured" in Step 2.

## 2. Plan
- **Step 1**: In `NewPolicyWizard.tsx`, modify the `handleNext` function. When transitioning from Step 1 (Details) to Step 2 (Financials), inspect the `details` data.
- **Step 2**: Identify if a "Value" or "Sum Insured" like key exists in the `details` object (case-insensitive, e.g., "value", "value kshs.", "sum insured").
- **Step 3**: If found, update the `financials.sumInsured` state with this value.
- **Step 4**: Pass this pre-filled `financials` state to `StepFinancials`.

## 3. Atomic Steps
- [x] **Step 3.1**: Update `handleNext` in `frontend/src/components/Insurance/Wizard/NewPolicyWizard.tsx` to implement the sync logic.
- [x] **Step 3.2**: Verify that the value entered in Step 1 correctly populates the "Sum Insured" field in Step 2.
