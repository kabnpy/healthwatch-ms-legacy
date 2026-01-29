# Project Status (Session End: 2026-01-28)

## Finished
- **Financial System Overhaul (Merged)**
    - Decoupled Underwriting (Risk Notes) from Billing (Invoices).
    - Implemented `Invoice`, `InvoiceLineItem`, `Receipt`, and `ReceiptAllocation` models.
    - Added automatic invoicing logic to the Risk Note creation flow.
    - Verified with new API tests in `test_financials.py`.
- **UI Refinement & Standardization**
    - **Human-Readable Policy Titles**: Implemented `display_name` (e.g., "Motor Private - KDF 334K") across the backend and frontend.
    - **Standardized Status Indicators**: Created a reusable `StatusIndicator` component following the Admin page style (colored dot + text).
    - **Client Table Improvements**: Added "Contact Person" column and visual badges for Client Type (Individual/Corporate).
- **Navigation & UX Refinement**
    - Implemented dynamic Breadcrumbs and a global `CommandMenu` (Ctrl+K).
    - Refactored Client Hub and Policy Dashboard into true nested routes.
    - Standardized all data tables with real-time filtering and action menus.
- **Unified Document System**
    - Created `UniversalDocumentViewer` using a loader-based architecture.
    - Standardized `RiskNoteTemplate` and `InvoiceTemplate` visuals.
    - Cleaned up redundant Certificate views.
- **System Stability**
    - Fixed backend relationship mapping errors and 404 routing issues.
    - Optimized frontend bundle via code-splitting improvements.

## Next Steps
1. **Frontend Financials**: Implement the "Payments & Invoicing" dashboard to allow users to manually create Receipts and allocate them to Invoices.
2. **File Uploads**: Transition the `DocumentManager` from simple URL strings to actual file uploads (using S3 or local storage).
3. **Endorsement Wizard**: Add specific UI logic for the "Modify/Endorse" transaction type in the Policy Dashboard.

## Architectural Decisions
- **Decoupled Financials**: Invoices now act as the primary billing entity, allowing N Risk Notes to be grouped into 1 Invoice.
- **Loader Pattern**: The `UniversalDocumentViewer` uses internal loader components to prevent unnecessary/failing API calls when switching document types.
- **Explicit Routing**: Backend router prefixes are now defined explicitly in `app/api/main.py` to prevent accidental double-prefixing.
