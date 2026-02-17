# UI Standardization & Client Management Strategy

## 1. The "Clean Table" Standard
To resolve the inconsistency between Client (Links) and Policy (Buttons) tables:
- **Rule:** The primary column (Name, Policy Number) MUST be a clickable `<Link>`.
- **Rule:** Explicit "View" buttons are deprecated.
- **Rule:** Action-heavy buttons (e.g., "Add Risk Note") are removed from global tables and moved to their respective Detail Views.
- **Rule:** Every table will use a `DropdownMenu` for secondary actions (Edit, Delete, Copy ID).

## 2. Client Management Lifecycle
We will implement a two-tier management system for ergonomics and safety.

### Tier 1: Quick Actions (Listing)
- In the `Clients` table, add an `Actions` column with:
    - Edit (Opens a slide-over/dialog).
    - Copy Client ID.
    - Go to Financials.

### Tier 2: Dedicated Management (Detail View)
- Add a **Settings** tab to the Client Hub (`/clients/$clientId/settings`).
- **Content:**
    - Full Edit Form (Name, KRA PIN, Address, Contact).
    - **Danger Zone:** A visually distinct section at the bottom for "Archive" or "Delete" actions.
    - **Reasoning:** Destructive actions should be behind an intentional navigation step to prevent accidental clicks.

## 3. Policy Action Migration
- **Remove:** `AddRiskNote` component from `frontend/src/components/Policies/columns.tsx`.
- **Move to:** `frontend/src/routes/_layout/policies.$policyId.tsx`.
- **UX Integration:** Place the action within the "Quick Actions" card or a dedicated "Endorsements" tab. This ensures the user has reviewed the current policy state before adding a new financial transaction.

## 4. Implementation Checklist
- **[ ] Standardize Client Table:** Add action menu, ensure name is the link.
- **[ ] Standardize Policy Table:** Remove "View/Add" buttons, make Policy Number the link, add action menu.
- **[ ] Create Client Settings Route:** Implement the `/settings` nested route for clients.
- **[ ] Implement Client Edit Form:** Create a reusable form component for editing client details.
- **[ ] Policy Dashboard Update:** Integrate "Add Risk Note" into the Policy Dashboard UI.
