# Strategy: Motor Private Premium Calculator & Benefits Refinement

## Goal
Implement a sophisticated premium calculation engine for "Motor Private" policies that supports tiered rates, minimum premiums, and "High-End" inclusive benefits. Additionally, rename "Extensions" to "Benefits" and add "OM Rescue Plus".

## 1. Requirements Analysis

### Tiered Rate Structure (Motor Private)
| Sum Insured Range (KES) | Rate (%) | Minimum Premium (KES) | Notes |
| :--- | :--- | :--- | :--- |
| 0 - 1,500,000 | 5.00% | 60,000 | |
| 1,500,001 - 2,500,000 | 4.00% | 75,000 | |
| 2,500,001 - 3,000,000 | 3.50% | 100,000 | |
| 3,000,001 - 5,000,000 | 3.25% | - | High-End (All Inclusive) |
| 5,000,001+ | 3.00% | - | High-End (All Inclusive) |

### "High-End" Logic (Sum Insured >= 3,000,000)
- **Inclusive Benefits**: Political Violence & Terrorism (PVT) and Excess Protector are included in the basic premium (cost = 0).
- **Standard Logic (< 3M)**: PVT and Excess Protector are chargeable at 0.25% of Sum Insured each.

### New Benefit: OM Rescue Plus
- **Cost**: Flat fee of KES 1,000.
- **Applicability**: Optional add-on for Motor Private.

### Terminology
- Rename "Extensions" to "Benefits" in the UI.

## 2. Technical Implementation Plan

### A. Refactor Calculator Service (`frontend/src/lib/calculator.ts`)
- Create a dedicated `calculateMotorPrivatePremium` function.
- Implement the tiered rate selection logic.
- Implement the minimum premium checks.
- Implement the conditional logic for PVT/Excess pricing based on the 3M threshold.
- Add `omRescuePlus` to the input and breakdown.

### B. Update Financials Step (`StepFinancials.tsx`)
- **Rename**: Change "Motor Extensions" section header to "Benefits".
- **New Field**: Add a checkbox for "OM Rescue Plus" (default: false).
- **Rate Input**:
    - For Motor Private, make the "Rate" field **read-only** or **disabled**. It should be automatically set based on the Sum Insured.
    - Display the applied rate to the user.
- **High-End UX**:
    - If `sumInsured >= 3,000,000`:
        - Automatically check PVT and Excess Protector.
        - Disable these checkboxes (force selected).
        - Show a badge or note: "High-End: All Inclusive".
- **Premium Preview**: Update to show the breakdown correctly (e.g., PVT: 0.00 (Included)).

## 3. Atomic Steps
- [x] **Step 3.1**: Update `frontend/src/lib/calculator.ts` with the new logic.
- [x] **Step 3.2**: Update `frontend/src/components/Insurance/Wizard/StepFinancials.tsx` to integrate the new calculator, rename sections, and add the "OM Rescue Plus" field.
- [x] **Step 3.3**: Verify the calculation tiers and "High-End" behavior in the wizard.
