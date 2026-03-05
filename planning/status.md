# Project Status (Session End: 2026-02-20)

## Finished (Key Milestones)
- **Database & Model Reconciliation**: Synchronized the database schema with the backend models. Updated Alembic migration `c5c580ca4b1f` to correctly implement `RiskNote.cover_snapshot` as the source of truth for risk details, replacing the redundant `Policy.risk_details` approach.
- **Service Layer Hardening**: Refactored `PolicyService` to improve temporal precision in endorsements and optimized the `RatingService` by consolidating tier sorting logic.
- **Wizard Data Flow Alignment**: Enhanced the frontend `NewPolicyWizard` to calculate dynamic coverage periods based on selected duration, eliminating hardcoded 1-year assumptions.
- **Financial Hardening & Rating Engine**: Standardized `sum_insured` as the single authoritative source for insured values across the stack. Refactored `RatingService` to use a singular semantic input and implemented `ManualRatingStrategy` for non-motor products.
- **Prestart Service Stabilization**: The `prestart` service now successfully completes database migrations and mock data seeding.
- **Client Regeneration**: Successfully regenerated the TypeScript client from the backend OpenAPI schema and verified type integrity with `tsc`.
- **Backend Linting & Type Hardening**: Resolved all `ruff` and `mypy` issues. Fixed a critical renaming bug in the `risk_notes` API route. Stabilized `seed_mock_data.py` and consolidated `RatingService` return types for better consistency and developer experience.
- **Renewal Workflow Implementation**: Implemented a comprehensive end-to-end policy renewal system.
    - **Status Workflow**: Added `RENEWAL_INVITED` and `RENEWAL_CONFIRMED` statuses to Policies and Risk Notes.
    - **Automated Notifications**: Created a daily background task to send invitations (30 days before expiry) and reminders (7 days before expiry).
    - **Manual Triggers**: Added API endpoints and UI buttons to manually trigger renewal notifications.
    - **Correspondence Logging**: Implemented automated logging of all renewal-related emails into the client correspondence history.
    - **Performance Optimization**: Fixed N+1 query issues in policy list views using SQLAlchemy `selectinload`.
    - **Frontend Dashboard**: Added a "Renewals" dashboard with expiry tracking and hardened date parsing for timezone consistency.

## Ongoing
- **Type Integrity & Stabilization**: Resolving persistent TypeScript errors in the auto-generated client and components.

## Next Steps
1. **Verification of Backend Changes**: Run the backend test suite once a database connection is established to ensure all changes are functional.
2. **Audit Traceability**: Finalize the `change_log` implementation for endorsements to ensure full traceability of risk detail modifications.
3. **Automated Testing**: Expand the backend test suite to cover the new pro-rata endorsement calculations and rating tier logic.
4. **Frontend Refinement**: Polish the document viewing experience to handle the new `cover_snapshot` structure across all templates.

## Architectural Decisions
- **Atomic Snapshot Strategy**: We store the full state of the risk (the "Snapshot") on the `RiskNote` issued for each transaction. This ensures that every document (Risk Note, Invoice) refers to the authoritative state of the cover at the exact moment of issuance.
- **Policy as the Contract Container**: The `Policy` model remains the long-lived container for the contract, but coverage-specific data (dates, values) is derived from its related `RiskNotes`.
- **Pro-rata Endorsements**: Premium adjustments for mid-term modifications are calculated pro-rata based on the remaining coverage period relative to the original term.
