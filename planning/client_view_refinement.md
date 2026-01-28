# Client View Refinement & Card Standardization Strategy

## 1. Objective
Improve the ergonomics and consistency of the Client Hub and Policy Dashboard by standardizing summary components and decluttering the main layout.

## 2. Component Standardization: The "Summary Card"
Currently, both Client and Policy views use custom-coded cards for high-level details. We will create a unified `InfoCard` or `SummaryCard` component.
- **Location:** `frontend/src/components/Common/SummaryCard.tsx`
- **Features:** Icon support, Label, Value (with support for sub-text/mono-font), and optional "Status" badge integration.

## 3. Client Hub Layout Refactor (`/clients/$clientId`)
The current layout has 4 large cards fixed at the top, pushing the primary content (Tabs) down.
- **Change:** Add an **Overview** tab as the default view.
- **Action:** Move the KRA PIN, Email, Phone, and Client Type cards inside the Overview tab.
- **Result:** The header remains slim (Name/Type only), and the detail content is contextualized.

## 4. Policy Dashboard Refinement (`/policies/$policyId`)
Standardize the summary cards and evaluate "Quick Actions."
- **Action:** Replace existing summary implementations with the new `SummaryCard`.
- **Quick Actions Evaluation:** Move "Print" actions to the specific document tabs or a "More" menu in the header to free up primary real-estate. Keep "Renew/Endorse" as primary actions.

## 5. Stepwise Implementation Plan

### Phase 1: Standard Component
- [x] Create `frontend/src/components/Common/SummaryCard.tsx`.
- [x] Migrate `frontend/src/routes/_layout/clients.$clientId.tsx` to use `SummaryCard`.

### Phase 2: Client Hub Tab Migration
- [x] Refactor `frontend/src/routes/_layout/clients.$clientId.tsx` to include the `Overview` tab.
- [x] Move cards from header to `Overview` tab content.
- [x] Ensure default route redirects to `/overview`.

### Phase 3: Policy View Alignment
- [x] Update `frontend/src/routes/_layout/policies.$policyId.tsx` summary section.
- [x] Standardize the "Quick Actions" layout to match the new dashboard aesthetic (integrated into PolicyHeader).

## 6. Progress Tracking
- **[2026-01-28]:** Strategy created. Phases 1, 2, and 3 completed.
