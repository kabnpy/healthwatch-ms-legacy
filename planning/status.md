# Project Status

## Finished
- **MVP Step 1: Backend Data Injection**
    - Created `backend/app/seed_mock_data.py`.
    - Generated and applied Alembic migration (`835e5ddfd056`) for insurance models (Fixed missing tables issue).
    - Seeded database with Jubilee Insurance, Motor Product, John Doe client, and an active policy.
- **Backend API Extension**
    - Implemented `backend/app/api/routes/risk_notes.py` with CRUD endpoints.
    - Registered `risk_notes` router in `backend/app/api/main.py`.
- **MVP Step 2: TS Client Generation**
    - Regenerated `frontend/src/client` to include new insurance endpoints.
- **MVP Step 3: Smart Hooks**
    - Created `frontend/src/hooks/useInsurance.ts` with TanStack Query hooks.
- **MVP Step 4: UI Development (Workflow Foundation)**
    - **Navigation:** Added "Clients" to the sidebar.
    - **Client List:** Created `_layout/clients.index.tsx` and added "Add Client" form.
    - **Client Hub:** Refactored `_layout/clients.$clientId.tsx` to precisely match the reference implementation pattern (single suspense boundary, consolidated data fetching).
    - **Risk Note Form:** Implemented `components/Insurance/RiskNoteForm.tsx` with automatic premium/levy calculator.
    - **Print System:** Created `routes/print/risk-notes.$id.tsx` mimicking official insurance document layouts.
- **Maintenance & Stability**
    - **Frontend Build Fix:** Resolved `react-hook-form` resolution and type errors in `RiskNoteForm.tsx`.
    - **TypeScript Cleanup:** Systematically added type annotations and fixed `any` errors in `AddUser`, `AddItem`, `AddClient`, and `AddPolicy` forms.
    - **Hook Repair:** Restored corrupted `useInsurance.ts` and added `useProducts` hook.
    - **Database Sync:** Fixed `relation "insurer" does not exist` error by generating and applying correct Alembic migrations.
- **MVP Phase 2: Complex Views & Modeling**
    - **Data Modeling:** Updated `RiskNote` to support JSON-based premium breakdown and snapshots. Replaced `physical_address` with `postal_address` for Clients.
    - **Migrations:** Applied schema changes (`0963bb59be04`) and updated existing records.
    - **Calculation Engine:** Created `frontend/src/lib/calculator.ts` for centralized premium logic.
    - **Dual-Mode Print:** Enhanced print view to support `?mode=invoice` (Financials) and `?mode=certificate` (Benefits).
    - **UI Enhancements:** Refactored `RiskNoteForm` to include "PVT" and "Excess Protector" toggles with live price updates.
    - **Document Viewer:** Implemented a reusable `DocumentViewerModal` and integrated it into the Client Hub, allowing users to view and print Risk Notes without leaving the page.
    - **Policy Dashboard:** Created a dedicated "Command Center" (`/policies/$policyId`) aggregating Policy, Risk Item, and Risk Note data into a tabbed interface with "Overview", "History", and "Documents".
- **MVP Phase 3: New Business Wizard**
    - **API Extension:** Added `POST /policies/{id}/risk-items` endpoint to backend.
    - **Stepper UI:** Implemented `NewBusinessWizard` modal with 3 steps: Asset Details, Coverage & Financials, and Review.
    - **Transaction logic:** Wizard coordinates creating Policy, Risk Item, and Risk Note in a single flow.
    - **Real-time Math:** Integrated calculation engine with live preview in the financials step.

## Next Steps
1. **Verification:** Test the "New Business Wizard" flow end-to-end.
2. **Implementation:** Add "Renew" and "Endorse" logic using the wizard in different modes.
3. **UI Polish:** Enhance the Client Hub with more detailed summaries and better empty states.

## Architectural Decisions
- **Domain Routing:** Created a dedicated `risk-notes` backend router rather than nesting everything under policies for better scalability.
- **File-based Routing:** Used `clients.index.tsx` and `clients.$clientId.tsx` to handle the transition from list to hub view.
- **Print View:** Dedicated `/print` route namespace to allow for clean, sidebar-free document generation.
- **Type Safety:** Enforced strict `ApiError` casting and Zod schema typing for all new forms to ensure build stability.
- **Resilient UI:** Adopted the reference "Items" pattern for all data-driven views to ensure graceful loading and empty states.
- **JSON for Flexibility:** Moved from rigid float columns (`basic_premium`, etc.) to a `premium_breakdown` JSON column to allow for variable levies and dynamic extensions without frequent schema migrations.
- **Modal-Based Viewing:** Shifted from separate print pages to a modal-based document viewer to improve UX and prepare for future document types (PDFs/Images).
- **Dashboard Aggregation:** Utilized a composite hook (`usePolicyDashboard`) to fetch and correlate data from multiple services (Policy, RiskNotes, RiskItems) for a unified UI.
- **Wizard Pattern:** Implemented a stepper-based wizard for complex data entry to guide users through the "Policy Issuance" workflow, ensuring all required related entities (Asset, Transaction) are created together.