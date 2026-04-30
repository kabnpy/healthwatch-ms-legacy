# Specification: System Architecture Refinement & Hardening

## Overview
This track focuses on evolving the system's architectural integrity by strictly decoupling business logic from data models on the backend, modularizing complex frontend route files, and establishing robust end-to-end (E2E) testing for critical business workflows.

## Functional Requirements

### 1. Backend: Domain Logic Decoupling
- **Service Layer Consolidation**: Migrate all business logic currently residing within SQLModel classes (e.g., `calculate_premium`, `validate_risk_details`) into dedicated Service classes (e.g., `ProductService`, `PolicyService`).
- **Anemic Models**: Ensure models act strictly as data schemas and relationship definitions.
- **Dependency Management**: Standardize the use of `SessionDep` and service orchestration within the API and service layers.

### 2. Frontend: Modularization & Consistency
- **God Route Refactoring**: Decompose large route files, specifically the Policy Dashboard (`clients.$clientId.policies.$policyId.tsx`), into reusable, domain-focused sub-components (e.g., `TransactionHistory`, `PolicyActionsToolbar`).
- **Centralized Document Utilities**: Implement a unified frontend `DocumentService` or utility module to handle URL construction, format switching, and authenticated downloads for all document types (Risk Notes, Invoices, Renewals).
- **Error Boundary Treatment**: Standardize the application of Error Boundaries and Fallback UIs across all major application segments to ensure a graceful failure experience.

### 3. Automated Testing: E2E Coverage
- **Playwright Implementation**: Create end-to-end tests using Playwright for the following critical paths:
    - **Policy Wizard**: Completing Step 1 through Step 3 and successfully issuing a Risk Note.
    - **Renewal Workflow**: The full cycle from "Renewal Invited" state to generating and viewing the Invitation document.
    - **Document Actions**: Verifying that viewing, printing, and downloading documents works correctly across different browsers.

## Acceptance Criteria
- [ ] Backend models are free of business logic methods and local service imports.
- [ ] Large frontend route files are decomposed into components of manageable size (< 200 lines where practical).
- [ ] A single source of truth exists for all document-related API interactions in the frontend.
- [ ] New Playwright E2E tests are integrated into the CI/CD pipeline and pass reliably.
- [ ] Code follows all established style guides and maintains >80% unit test coverage for new service logic.

## Out of Scope
- Implementing new insurance classes beyond those currently supported.
- Transitioning to an asynchronous task queue for PDF generation (reserved for a future track).
- Major UI/UX redesigns.
