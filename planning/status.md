# Project Status (Current Session: 2026-03-12)

## Finished (Key Milestones)
- **Database & Model Reconciliation**: Synchronized the database schema with the backend models. Updated Alembic migration `c5c580ca4b1f` to correctly implement `RiskNote.cover_snapshot` as the source of truth for risk details, replacing the redundant `Policy.risk_details` approach.
- **Service Layer Hardening**: Refactored `PolicyService` to improve temporal precision and optimized the `RatingService` by consolidating tier sorting logic.
- **Wizard Data Flow Alignment**: Enhanced the frontend `NewPolicyWizard` to calculate dynamic coverage periods based on selected duration, eliminating hardcoded 1-year assumptions.
- **Financial Hardening & Rating Engine**: Standardized `sum_insured` as the single authoritative source for insured values across the stack. Refactored `RatingService` to use a singular semantic input and implemented `ManualRatingStrategy` for non-motor products.
- **Prestart Service Stabilization**: The `prestart` service now successfully completes database migrations and mock data seeding.
- **Client Regeneration**: Successfully regenerated the TypeScript client from the backend OpenAPI schema and verified type integrity with `tsc`.
- **Backend Linting & Type Hardening**: Resolved all `ruff` and `mypy` issues. Fixed a critical renaming bug in the `risk_notes` API route. Stabilized `seed_mock_data.py` and consolidated `RatingService` return types for better consistency and developer experience.
- **Renewal Workflow Implementation**: Implemented a comprehensive end-to-end policy renewal system.
- **Modularization of Models & CRUD**: Refactored `backend/app/models.py` and `backend/app/crud.py` into domain-specific modules with unified exports.
- **One-page A4 Risk Note PDF Generation**:
    - Integrated **WeasyPrint** for high-fidelity PDF generation from HTML/Jinja2 templates.
    - Designed a dense, single-page A4 layout optimized for insurance risk notes.
    - Implemented `DocumentService` in the backend for automated PDF production.
    - **Frontend Polish**: Fixed `displayName` regression and added a "Digital vs PDF" view toggle in the Policy Dashboard.
    - **History Integration**: Added PDF view/download actions to the transaction history timeline and table.

## Ongoing
- **Type Integrity & Stabilization**: Finalizing TypeScript type refinements across the modularized models.

## Next Steps
1. **Merge `feat/one-page-risknote`**: Finalize and merge the PDF generation track into `main`.
2. **Financial Hardening (Invoices)**: Extend PDF generation to Invoices (similar to Risk Notes).
3. **Audit Trail Reinforcement**: Re-evaluate requirements for the postponed audit hardening track.

## Architectural Decisions
- **Atomic Snapshot Strategy**: We store the full state of the risk (the "Snapshot") on the `RiskNote` issued for each transaction. This ensures that every document (Risk Note, Invoice) refers to the authoritative state of the cover at the exact moment of issuance.
- **Policy as the Contract Container**: The `Policy` model remains the long-lived container for the contract, but coverage-specific data (dates, values) is derived from its related `RiskNotes`.
- **Hybrid Document Viewing**: We maintain both an interactive "Digital View" (for editing drafts) and a "PDF View" (for official documentation) within the frontend.

## Future Optimizations
- **Policy Expiry Denormalization**: Consider denormalizing `current_coverage_end` onto the `Policy` model to improve query performance.
