# Project Status (Session End: 2026-02-20)

## Finished (Key Milestones)
- **Financial Hardening & Rating Engine**: Standardized `sum_insured` as the single authoritative source for insured values across the stack. Refactored `RatingService` to use a singular semantic input and implemented `ManualRatingStrategy` for non-motor products.
- **Wizard Data Flow Alignment**: Eliminated duplicate data paths ('Value Kshs.' vs 'sum_insured') in the frontend wizard, ensuring seamless value synchronization between asset capture, financial calculation, and the final review step.
- **Semantic Model Cleanup**: Removed legacy field aliases from backend Pydantic schemas, enforcing a clean and consistent data model for policy risk details.
- **Frontend Routing & Policy View Refinement**: Resolved a routing conflict by converting `clients.$clientId.policies.tsx` to an index route (`clients.$clientId.policies.index.tsx`). Fixed a `queryKey` mismatch and optimized client data fetching.
- **CRUD Layer Hardening**: Fixed a widespread bug where SQLAlchemy `where` clauses used `is None` instead of `== None`, ensuring correct SQL generation for records with NULL values.
- **Prestart Service Stabilization**: The `prestart` service now successfully completes database migrations and mock data seeding.
- **Client Regeneration**: Successfully regenerated the TypeScript client from the backend OpenAPI schema and verified type integrity with `tsc`.
- **Policy Issuance Error Fix**: Resolved "Internal Server Error" (500) during policy creation by fixing Pydantic validators, Decimal serialization, and field mapping in `PolicyService`.
- **Motor Private Validation & Schema Refinement**: Removed the "Model" field from Motor Private schema, blueprints, and seed data. Improved `injectWizardData` in the frontend to resiliently handle both nested and flat input structures.
- **Risk Note & Invoice Refinement**: Significant enhancements to Risk Note generation, invoicing workflow, layout standardization, and dynamic cover display.
- **Simplified Insurance Models Refactor**: Streamlined core data models by merging RiskItem into Policy for a 1:1 relationship.

## Ongoing
- **Type Integrity & Stabilization**: Resolving persistent TypeScript errors in the auto-generated client and components.

## Next Steps
1. **Audit Hardening**: Implement robust auditing for all policy changes and ensure the transaction history is fully traceable.
2. **Automated Testing & CI/CD**: Implement a robust test suite and automate deployments via GitHub Actions.
3. **Comprehensive Documentation**: Complete the technical and user documentation for the current feature set.
4. **Production Monitoring**: Establish basic logging and monitoring for the Railway deployment.

## Architectural Decisions
- **Singular Semantic Truth**: We enforce `sum_insured` as the authoritative key for the primary value of any risk, regardless of how it's labeled in a specific template. This avoids data duplication and rating errors during state transitions.
- **Unified Policy Entity**: 1 Policy = 1 Cover Instance. This simplifies data capture and document generation significantly.
- **Audit via Deltas**: To ensure a single source of truth for the current state, we store only the authoritative record on the `Policy`. Audit history is preserved via the `change_log` (delta) on each `RiskNote` instead of using full-state snapshots.
- **Pro-rata Endorsements**: Premium adjustments for mid-term modifications are now calculated pro-rata based on the remaining coverage period.
