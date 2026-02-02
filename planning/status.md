# Project Status (Session End: 2026-02-02)

## Finished
- **Decoupled Rendering Logic**
    - **Frontend Layout Registry**: Moved presentation logic (grid vs. list) from the database to `frontend/src/utils/layoutRegistry.ts`.
    - **Robust Seeding**: Updated `seed_mock_data.py` with an upsert strategy to ensure existing products are synchronized with the latest schema changes.
    - **Clean Data Models**: Removed all frontend-specific metadata (`display_type`) from the product JSON schema.
- **Risk Note Template Refinement**
    - **List-Style Rendering**: Introduced `RiskNoteListItem` to support granular list layouts for "Benefits and Limits" sections.
    - **Display Type Control**: Added `display_type` metadata to `Product.product_details` to toggle between `table-row` and `list-item` layouts dynamically.
    - **Seed Data Enhancement**: Updated core product definitions (Motor, PA) to include categorized benefits as list items for improved readability.
- **Unified Product Schema & Dynamic Wizard**
    - **Manifest-Driven Architecture**: Centralized all product-specific details (benefits, excess, clauses) into the `Product.form_schema`, removing redundant attributes.
    - **Dynamic Wizard**: Refactored the "New Policy" wizard to dynamically render capture fields from the product schema, supporting product-agnostic data entry.
    - **Conditional Logic**: Implemented class-specific UI logic (e.g., hiding Sum Insured for Personal Accident) in the creation workflow.
    - **Agnostic Rendering**: Updated `RiskNoteTemplate` to aggregate both static and captured fields into a single professional layout.
- **Risk Note Refinement (Composable & Dynamic)**
    - **Dynamic Layouts**: Refactored `RiskNoteTemplate` to use a composable architecture (`RiskNoteRow`, `RiskNoteSection`) driven by `Product.form_schema`).
    - **Automatic Issuance Workflow**: Updated backend CRUD to automatically generate a "New Business" Risk Note (Draft) upon policy creation.
    - **Enriched Data Catalog**: Updated seeding with logical grouping (`section`) and visibility toggles (`show_in_risknote`) for all core products (Motor, PA, Domestic).
    - **Draft Workflow**: Implemented a "Populate & Issue" flow in the Policy Dashboard to finalize draft risk notes using a dynamic form renderer.
- **UI & UX Refinement**
    - **Document Viewer Scaling**: Implemented a "Fit-to-Width" scaling mechanism in `DocumentViewerModal` using `ResizeObserver`, ensuring A4 documents are readable on all screen sizes.
    - **Expanded Modal Layouts**: Standardized complex modals (`AddClient`, `AddPolicy`, `AddRiskNote`) to `max-w-2xl` and the document viewer to `95vw` to eliminate the "cramped" feel.
    - **BaseDocument Optimization**: Removed redundant overflow and layout constraints to support dynamic scaling and improved typography (Sans-serif).
- **Minimal Invoice Design**
    - Updated `Letterhead` to use the new centered address block and HealthWatch details.
    - Refactored `BaseDocument` to support the centered Title/[Reference] header style.
    - Completely redesigned `RiskNoteTemplate` and `InvoiceTemplate` to match the "Minimal Invoice" layout (Client Left, Dates Split, Grid Table, Financial Footer).
- **Refined Architecture Implementation (Major Overhaul)**
    - **Temporal Versioning**: Implemented history tracking for `RiskItems` using `version_number` and `valid_from` fields.
    - **Transaction Snapshots**: `RiskNotes` now capture a frozen state of assets (`items_snapshot`) for financial and legal auditability.
    - **Polymorphic Documents**: Unified document storage system supporting links to Clients, Policies, Claims, and Receipts (Proof of Payment).
    - **Multi-Contact System**: Corporate clients can now have multiple contact persons stored in a flexible JSON structure.
- **Financial System Integrity**
    - **Reversals**: Implemented `void_receipt` logic that automatically restores invoice balances and statuses.
    - **Audit Trail**: Created `AllocationHistory` to track exactly which payments settled which debts.
- **UI Standardization**
    - **Human-Readable Policies**: Switched from raw numbers to descriptive titles (e.g., "Motor Private - KCA 123B").
    - **Standardized Indicators**: Universal `StatusIndicator` component applied across Admin, Clients, and Policies.

## Next Steps
1. **Frontend Build Verification**: Finalize TypeScript fixes in `DocumentViewer.tsx` and `RiskNoteForm.tsx` to ensure a clean production build after system restart.
2. **Infrastructure Stability**: Resolve the Traefik-to-Docker-Daemon connectivity issue that caused intermittent 404s during rapid reloads.
3. **Frontend Financials**: Implement the "Payments & Invoicing" dashboard to allow users to manually create Receipts and allocate them to Invoices.
4. **File Uploads**: Transition the `DocumentManager` from simple URL strings to actual file uploads (using S3 or local storage).

## Architectural Decisions
- **Decoupled Financials**: Invoices now act as the primary billing entity, allowing N Risk Notes to be grouped into 1 Invoice.
- **Loader Pattern**: The `DocumentViewer` uses internal loader components to prevent unnecessary/failing API calls when switching document types.
- **Explicit Routing**: Backend router prefixes are now defined explicitly in `app/api/main.py` to prevent accidental double-prefixing.
- **Migration Sync Strategy**: When rolling back branches, always verify `alembic_version` matches the branch head to prevent "missing revision" errors.
