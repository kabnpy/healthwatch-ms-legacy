# Project Status (Session End: 2026-02-17)

## Finished (Key Milestones)
- **Frontend Routing & Policy View Refinement**: Resolved a routing conflict by converting `clients.$clientId.policies.tsx` to an index route (`clients.$clientId.policies.index.tsx`). Previously, it was acting as a layout for sub-routes but lacked an `<Outlet />`, which blocked specific policy views. Also fixed a `queryKey` mismatch, optimized client data fetching, and improved the `activeTab` detection logic.
- **CRUD Layer Hardening**: Fixed a widespread bug where SQLAlchemy `where` clauses used `is None` instead of `== None`, which caused incorrect SQL generation and failed to retrieve records with NULL values. This resolved the `404: Policy not found` errors during mock data seeding.
- **Prestart Service Stabilization**: The `prestart` service now successfully completes database migrations and mock data seeding.
- **Client Regeneration**: Successfully regenerated the TypeScript client from the backend OpenAPI schema and verified type integrity with `tsc`.
- **Policy Issuance Error Fix**: Resolved "Internal Server Error" (500) during policy creation. Fixed three root causes:
    1. Added Pydantic validators to `MotorPrivateRiskDetails` to handle numeric strings with commas (e.g., "1,500,000").
    2. Converted Decimal values to floats in `calculate_levies` to ensure JSON serializability for database storage.
    3. Corrected field mapping in `PolicyService` from `levies` to `taxes` to align with the `RiskNote` model and database schema.
    4. Wrapped premium calculation in `PolicyService` within a try-except block to return 400 Bad Request instead of 500 Internal Server Error for calculation failures.
- **Motor Private Validation & Schema Refinement**: Removed the "Model" field from Motor Private schema, blueprints, and seed data. Improved `injectWizardData` in the frontend to resiliently handle both nested and flat input structures, ensuring proper mapping of wizard data to document blueprints.
- **Motor Private Validation Fix**: Resolved policy creation failure by correcting `injectWizardData` in the frontend to handle nested blueprint structures. Updated the backend `MotorPrivateRiskDetails` schema and `PolicyService` to support flexible type coercion and nested data extraction.
- **Risk Note & Invoice Refinement**: Significant enhancements to Risk Note generation, invoicing workflow, layout standardization, and dynamic cover display.
- **Standardized Wizard Layout**: Improved user experience and responsiveness for the New Policy Wizard.
- **Motor Private Premium Calculator**: Implemented complex premium calculation logic for Motor Private policies.
- **Policy Wizard Value Sync**: Automated data transfer between wizard steps for improved efficiency.
- **Client & Policy UI Refinements**: Standardized table views, status indicators, and address granularity.
- **Simplified Insurance Models Refactor**: Streamlined core data models by merging RiskItem into Policy for a 1:1 relationship, including backend and database changes, and frontend adaptation.
- **Unified Document Upload & Management**: Consolidated file handling into a single robust workflow for uploads and viewing.

## Ongoing
- **Type Integrity & Stabilization**: Resolving persistent TypeScript errors in the auto-generated client and components.

## Next Steps
1. **Automated Testing & CI/CD**: Implement a robust test suite and automate deployments via GitHub Actions.
2. **Comprehensive Documentation**: Complete the technical and user documentation for the current feature set.
3. **Production Monitoring**: Establish basic logging and monitoring for the Railway deployment.

## Architectural Decisions
- **Unified Policy Entity**: 1 Policy = 1 Cover Instance. This simplifies data capture and document generation significantly.
- **Temporal Integrity via Snapshots**: Auditing is preserved by capturing the full Policy state in each Risk Note transaction.