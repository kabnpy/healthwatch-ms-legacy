# Strategy: Dynamic Wizard Modal Styling

## Goal
Update the styling of the "New Policy Wizard" modal to be more flexible, allowing it to expand with its content instead of having a fixed/restricted width. This resolves layout issues in steps with high information density (e.g., StepFinancials with preview).

## 1. Analysis
- **Current Component**: `NewPolicyWizard.tsx` uses `DialogContent` with `max-w-4xl`.
- **Default UI Styles**: `ui/dialog.tsx` has `w-full max-w-[calc(100%-2rem)]` and `sm:max-w-lg`.
- **Issue**: `max-w-4xl` is likely too small for the 3-column + 1-column layout in `StepFinancials`, especially on smaller "large" screens, causing the content to feel cramped or overflow vertically.

## 2. Plan (Revised)
- **Compact Modal**: Revert to `max-w-3xl` for better line-length readability.
- **Stacked Layout**: Abandon the 4-column split view in `StepFinancials`. Place the "Premium Preview" below the inputs as a high-contrast summary block.
- **Improved Hierarchy**: Use a dark theme for the Preview block to distinguish it clearly from the form inputs.

## 3. Atomic Steps
- [x] **Step 3.1**: Revert `NewPolicyWizard.tsx` to `max-w-3xl`.
- [x] **Step 3.2**: Refactor `StepFinancials.tsx` to use a stacked, 2-column grid within sections and a full-width dark Preview block at the bottom.
- [x] **Step 3.3**: Verify that the wizard is easy to read and fits within standard screen sizes without layout issues.
