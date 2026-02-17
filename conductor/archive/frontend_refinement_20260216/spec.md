# Specification: Frontend Aesthetic & Copy Refinement

## 1. Overview
This track transforms the HealthWatch MS interface from an experimental "Papermark" metaphor to a permanent "Modern and Minimal" identity. The focus is on using high-quality typography and intentional spacing to create a professional, efficient workspace for insurance administration.

## 2. Objectives
- **Structural Overhaul:** Replace the 3-column layout with an inset sidebar and breadcrumb-driven layered navigation.
- **Design Standardization:** Ensure 100% consistency in the use of the "Subtle Neutrals" palette and shared UI components.
- **Professional Documentation:** Redesign Risk Note and Invoice templates to mirror the structure and clarity of professional physical documents.
- **Copy Polish:** Refine all interface text—specifically action labels, feedback, and microcopy—to be direct, clear, and instructive.
- **Guideline Update:** Codify the "Modern and Minimal" design principles in the project's Product Guidelines.

## 3. Scope
- **Product Guidelines:** Update `conductor/product-guidelines.md` to reflect the new design language.
- **Global Layout:** Refactor `AppSidebar.tsx` (variant to 'inset') and the main layout containers to support layered navigation.
- **Document Templates:** Redesign `RiskNoteTemplate.tsx` and `InvoiceTemplate.tsx` with a grid-based, professional document aesthetic.
- **Component Audit:** Review all Shadcn/UI usage to ensure consistent borders, backgrounds, and spacing.
- **Copy Audit:** Review and update text in `NewBusinessWizard`, `EndorsementFlow`, and dashboard feedback toasts.

## 4. Acceptance Criteria
- 3-column layout is fully removed in favor of the inset sidebar and breadcrumbs.
- Risk Notes and Invoices look like structured physical documents when viewed/printed.
- All "Papermark" or "Folder" terminology is removed from the code and guidelines.
- The interface feels unified, with typography and spacing carrying the visual weight.
- All high-frequency action labels (buttons) and error messages follow the "Direct & Clear" guideline.

## 5. Out of Scope
- Introducing new functional modules or data models.
- Changing the underlying authentication or API logic.
