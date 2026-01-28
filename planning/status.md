# Project Status

## Finished
- **MVP Step 1: Backend Data Injection**
    - Created `backend/app/seed_mock_data.py`.
    - Generated and applied Alembic migrations for insurance models and schema updates.
    - Seeded initial data and fixed `prestart` service failures.
- **Backend API Extension**
    - Implemented CRUD endpoints for `risk_notes`, `policies`, and `correspondences`.
    - Added `POST /policies/{id}/risk-items` and `GET/POST /clients/{id}/correspondences`.
- **MVP Step 2: TS Client Generation**
    - Regenerated `frontend/src/client` to include all new insurance and correspondence endpoints.
- **MVP Step 3: Smart Hooks**
    - Created `frontend/src/hooks/useInsurance.ts` with TanStack Query hooks for Clients, Policies, RiskNotes, Products, RiskItems, and Correspondences.
- **MVP Step 4: UI Development**
    - **Navigation:** Added "Clients" to the sidebar.
    - **Client Hub:** Refactored with a single suspense boundary, aggregated data fetching, and dedicated tabs for Policies, Risk Notes, and Documents.
    - **Risk Note Form:** Implemented with automatic premium/levy calculator.
    - **Document Viewer:** Created reusable `DocumentViewerModal` and `RiskNoteDocument` components for viewing/printing.
- **MVP Phase 2: Complex Views & Modeling**
    - **Data Modeling:** Updated `RiskNote` to support JSON breakdowns. Switched Client to `postal_address`.
    - **Calculation Engine:** Centralized premium logic in `frontend/src/lib/calculator.ts`.
    - **Policy Dashboard:** Created `/policies/$policyId` command center.
- **MVP Phase 3: Generalized Wizard & Client Documents**
    - **Universal Wizard:** Upgraded `NewBusinessWizard` to handle any insurance class. Added Product Selection and dynamic asset fields (Motor vs. General).
    - **Client Documents:** Implemented the "Documents" tab in the Client Hub, allowing upload and viewing of client-level files (KRA PIN, IDs).
- **Navigation & UX Refinement**
    - **Breadcrumbs:** Implemented a dynamic breadcrumb system in the main header using Shadcn UI and a custom `useBreadcrumbs` hook.
    - **Nested Routing:** Refactored the Client Hub from state-based tabs to true nested routes (`/clients/$clientId/policies`, etc.) for better deep-linking and breadcrumb accuracy.
    - **Architecture:** Extracted a reusable `Header` component for the main layout.
- **UI Standardization & Client Management**
    - **Table Patterns:** Standardized Client and Policy tables with clickable identifiers and "Three-dot" action menus.
    - **Client Hub Upgrades:** Added **Settings** tab for full profile editing and a dedicated **Financials/Invoices** tab.
- **Financial System Architectural Overhaul**
    - **Decoupling:** Separated Risk Notes (Underwriting) from Invoices (Billing).
    - **New Models:** Implemented `Invoice`, `InvoiceLineItem`, `Receipt`, and `ReceiptAllocation`.
    - **Automation:** Risk Note creation now automatically triggers/updates client invoices.
    - **Validation:** Added comprehensive API tests for the new financial workflows (`test_financials.py`).
    - **Polish:** Implemented `UniversalDocumentViewer` for a consistent viewing experience across all document types.
- **Code Quality & Maintenance**
    - **Linting & Formatting:** Cleaned up all linting and formatting issues in both Backend (Ruff, MyPy) and Frontend (Biome).
    - **Bug Fixes:** Resolved `prestart` container exit due to schema mismatch (`physical_address` -> `postal_address`).

## Next Steps
1. **Verification:** Test non-motor policy issuance via the generalized wizard.
2. **Implementation:** Add "Renew" and "Endorse" logic using the wizard's multi-mode support.
3. **Enhancement:** Implement actual file uploads (currently using URL/Path strings).

## Architectural Decisions
- **Class-Based UI:** The wizard dynamically adapts its schema and UI based on the `class_of_insurance` of the selected product.
- **Composite Fetching:** Using custom hooks like `usePolicyDashboard` to provide a unified data object for complex screens.
- **JSON for Flexibility:** Moved from rigid float columns to `premium_breakdown` JSON to handle dynamic taxes and extensions.
- **ID Enforcement:** Updated API routes to enforce ID linkage from URL paths rather than relying solely on request bodies, resolving unused variable warnings and improving safety.