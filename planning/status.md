# Project Status (Session End: 2026-02-06)

## Finished
- **Invoice & Cover Refinement**:
    - **Explicit Invoicing (Wizard)**: Refactored backend to stop automatic invoice generation and implemented a Bulk Invoice API. Added a frontend `InvoiceWizard` component allowing users to explicitly select risk notes for invoicing.
    - **Enhanced Cover Display Names**: Implemented dynamic naming logic (e.g., "Motor Private - [Reg No]") in both backend `PolicyPublic` model and frontend utilities using recursive search for maximum robustness.
    - **Rendering Fidelity**: Fixed `[object Object]` display bugs in document templates and wizard reviews by implementing recursive object rendering and JSX-aware cell handlers.
    - **Type Integrity**: Introduced `EnhancedPolicy` and `EnhancedRiskNote` interfaces to eliminate `any` usage in core insurance components.
    - **Structured Data Capture**: Integrated `injectWizardData` to ensure captured policy details match the structured product blueprint.
    - **Build Recovery**: Achieved a clean production build after resolving several TypeScript and dependency issues.
- **Standardized Wizard Layout**: Refactored the New Policy Wizard to use a compact `max-w-3xl` modal with a stacked layout (Inputs then Preview), significantly improving readability and eliminating layout issues on smaller screens.
- **Motor Private Premium Calculator**: Implemented tiered rate logic with exclusive higher limits, "High-End" benefits (inclusive PVT/Excess), and "OM Rescue Plus" benefit for Motor Private covers.
- **Policy Wizard Value Sync**: Implemented logic to automatically transfer "Value" from Step 1 (Details) to "Sum Insured" in Step 2 (Financials) for percentage-based covers.
- **Standardized Client Table**:
    - Removed the "Primary Contact" column.
    - Unified the "Client Type" badge styling (removed visual distinction between Corporate and Individual).
- **Granular Postal Address Refinement**: Successfully split the single address field into `postal_number`, `postal_code`, and `town` across backend models, database, and all frontend components/templates.
- **Consolidated Semantic Layout (Information Density)**
    - **Unified Table Engine**: Refactored `RiskNoteTable` to render the *entire* document body within a single semantic `<table>`.
    - **Section Spanning**: Implemented section headers as internal table rows with `colSpan={2}`, improving visual flow and reducing vertical white space.
    - **High-Density Rendering**: Added specialized renderers for nested objects (Benefits) and lists (Clauses) to maximize glanceability.
    - **Consolidated Templates**: Updated `RiskNoteTemplate` to aggregate all data (Client, Cover, Financials, Auth) into a single optimized array.
- **Refined Semantic Rendering (Document Standardization)**
    - **Uniform Styling**: Applied the "Clean Bordered" aesthetic across all document tables (Headers, Risk, Financials, Footer).
    - **Semantic Accessibility**: Replaced label columns with `<th scope="row">` for better document structure.
    - **Template Integration**: Fixed missing `product_details` by merging Product Catalog data (benefits, clauses) with instance-specific risk details.
    - **Complex Value Support**: Implemented bulleted list rendering for arrays within table cells.
- **Semantic Risk Note Rendering Refactor**
    - **Introduced `RiskNoteTable`**: A semantic table-based renderer for cover details and templates.
    - **Refactored Templates**: Updated `RiskNoteTemplate` and `InvoiceTemplate` to use actual HTML tables (`<table>`, `<tr>`, etc.) for professional, consistent layout and improved accessibility.
    - **Modernized Schema Builder**: Updated the product schema builder to use the new table-based editing interface.
    - **Codebase Cleanup**: Removed redundant `RecursiveDocumentTable` and `RiskNoteRow` components.
- **Simplified Models Refactor (Backend & DB Completed)**
    - **Merged `RiskItem` into `Policy`**: Removed redundant model, CRUD, and API routes.
    - **Updated Snapshots**: Risk Notes now use `policy_snapshot` instead of `items_snapshot`.
    - **Database Migration**: Applied Alembic migration `300464e5e502` and seeded mock data.
- **Frontend Logic Migration**
    - Updated `useInsurance.ts`, components (`AssetCard`, `RiskNoteForm`, `NewPolicyWizard`), and templates (`RiskNoteTemplate`) to use the new model structure.

## Ongoing: Type Integrity & Stabilization
- **Frontend Build Recovery**: Resolving persistent TypeScript errors in the auto-generated client and components.

## Next Steps
1. **Frontend Stability**: Monitor the production build for any further TypeScript issues as new features are added.
2. **eTIMS Integration Prep**: Start planning for tax compliance (invoice number formatting and external API sync).

## Architectural Decisions
- **Unified Policy Entity**: 1 Policy = 1 Cover Instance. This simplifies data capture and document generation significantly.
- **Temporal Integrity via Snapshots**: Auditing is preserved by capturing the full Policy state in each Risk Note transaction.
