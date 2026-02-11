# Project Status (Session End: 2026-02-06)

## Finished (Key Milestones)
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
1. **Database Migration**: Apply `risk_note_number` changes to the live database.
2. **Frontend Stability**: Monitor the production build for any further TypeScript issues.
3. **eTIMS Integration Prep**: Start planning for tax compliance (invoice number formatting and external API sync).

## Architectural Decisions
- **Unified Policy Entity**: 1 Policy = 1 Cover Instance. This simplifies data capture and document generation significantly.
- **Temporal Integrity via Snapshots**: Auditing is preserved by capturing the full Policy state in each Risk Note transaction.