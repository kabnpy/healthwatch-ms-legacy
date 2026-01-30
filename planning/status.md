# Project Status (Session End: 2026-01-29)

## Finished
- **Unified Product Schema & Dynamic Wizard**
    - **Manifest-Driven Architecture**: Centralized all product-specific details (benefits, excess, clauses) into the `Product.form_schema`, removing redundant attributes.
    - **Dynamic Wizard**: Refactored the "New Policy" wizard to dynamically render capture fields from the product schema, supporting product-agnostic data entry.
    - **Conditional Logic**: Implemented class-specific UI logic (e.g., hiding Sum Insured for Personal Accident) in the creation workflow.
    - **Agnostic Rendering**: Updated `RiskNoteTemplate` to aggregate both static and captured fields into a single professional layout.
- **Risk Note Refinement (Composable & Dynamic)**
    - **Dynamic Layouts**: Refactored `RiskNoteTemplate` to use a composable architecture (`RiskNoteRow`, `RiskNoteSection`) driven by `Product.form_schema`.
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
1. **Frontend Financials**: Implement the "Payments & Invoicing" dashboard to allow users to manually create Receipts and allocate them to Invoices.
2. **File Uploads**: Transition the `DocumentManager` from simple URL strings to actual file uploads (using S3 or local storage).
3. **Endorsement Wizard**: Add specific UI logic for the "Modify/Endorse" transaction type in the Policy Dashboard.
4. **Receipt Standardization**: Consider moving `ReceiptTemplate` to use the new `BaseDocument` structure for consistency.

## Architectural Decisions
- **Decoupled Financials**: Invoices now act as the primary billing entity, allowing N Risk Notes to be grouped into 1 Invoice.
- **Loader Pattern**: The `DocumentViewer` uses internal loader components to prevent unnecessary/failing API calls when switching document types.
- **Explicit Routing**: Backend router prefixes are now defined explicitly in `app/api/main.py` to prevent accidental double-prefixing.
