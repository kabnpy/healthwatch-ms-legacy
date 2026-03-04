# Track Specification: Remove Endorsement Workflow

## Overview
The "Endorsement" workflow currently exists in the codebase as a distinct transaction type for policy changes. However, business requirements indicate that endorsements are handled by insurance companies directly. The internal system should instead record these changes by simply creating a new `RiskNote` snapshot for the policy. This track focuses on removing the specific endorsement logic, UI, and data models to simplify the system.

## Functional Requirements
- **Backend API:** Remove all API endpoints specifically dedicated to creating or managing "Endorsements".
- **Service Layer:** Remove methods in `PolicyService` and `RiskNoteService` (if any) that handle endorsement-specific logic.
- **Data Models:** Remove `Endorsement` related fields from the `RiskNote` schema or any separate `Endorsement` models if they exist. Ensure `RiskNote` remains the single point of truth for policy snapshots.
- **Frontend UI:**
    - Remove the "Endorse" button/action from the Policy Detail page and Insurance Dashboard.
    - Ensure users can still create a new `RiskNote` to record changes (likely through a "New Risk Note" or "Renew" flow, or a general "Update" flow if applicable).

## Non-Functional Requirements
- **Simplicity:** The removal should reduce the overall complexity of the policy transaction engine.
- **Data Integrity:** Ensure that removing endorsement-specific logic does not break the ability to create standard `RiskNote` snapshots.

## Acceptance Criteria
- [ ] No "Endorsement" specific endpoints are visible in the API documentation (`/docs`).
- [ ] No "Endorse" button is present in the frontend UI.
- [ ] The `RiskNote` model is free of endorsement-specific fields or statuses.
- [ ] Creating a new `RiskNote` snapshot still works correctly for recording policy updates.
- [ ] All tests related to endorsements are removed or refactored to use standard Risk Notes.

## Out of Scope
- Migrating existing endorsement data (since it's confirmed that no such data exists yet).
- Modifying the core "New Business" or "Renewal" workflows, except where they shared logic with endorsements.
