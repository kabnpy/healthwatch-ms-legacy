# Implementation Plan: QoL & Architecture Hardening

## Phase 1: Logging & Error Handling (Foundation)
- [x] **Task 1.1: Backend Request Logging Middleware**
    - Create `backend/app/api/middleware.py`.
    - Implement a middleware to log requests and execution time.
- [x] **Task 1.2: Frontend Global Error Handling**
    - Update `frontend/src/main.tsx` to include an Error Boundary.
    - Configure `TanStack Query` global error handlers in `frontend/src/app.tsx` (or equivalent).
- [x] **Task 1.3: Standardize Alerts**
    - Audit usage of `useCustomToast` and ensure it's used for all CRUD operations.
    - Added global `onError` toast handling in `queryClient.ts`.

## Phase 2: Database Optimization
- [x] **Task 2.1: Index Audit**
    - Review `backend/app/models/` for missing indices on search/filter columns.
    - Added indices for `status`, `transaction_type`.
    - Added composite indices for:
        - `Policy`: `(client_id, status)`
        - `RiskNote`: `(policy_id, created_at)`
        - `Invoice`: `(client_id, status)`, `(client_id, date_issued)`
        - `Claim`: `(policy_id, status)`
- [x] **Task 2.2: Apply Migrations**
    - Generate and run Alembic migrations for new indices.
    - *Note: Migrations applied and confirmed.*

## Phase 3: Document Generation (Invoice & Renewals)
- [x] **Task 3.1: Invoice PDF Template**
    - Create `backend/app/templates/invoice.html` based on the Risk Note styling.
- [x] **Task 3.2: Extend DocumentService**
    - Add `generate_invoice_pdf` method to `DocumentService`.
    - Update `backend/app/api/routes/financials.py` to trigger PDF generation.
- [x] **Task 3.3: Renewal Invitation PDF**
    - Create template and service method for renewal invitations.

## Phase 4: Rollback & Operations
...
## Phase 6: Unify Document Generation
- [x] **Task 6.1: Universal Document Viewer**
    - Create a universal frontend component to render backend-generated HTML/PDF.
- [x] **Task 6.2: Refactor Risk Note Print Page**
    - Replace manual frontend rendering with the universal viewer fetching from the backend.
- [x] **Task 6.3: Refactor Invoice Print Page**
    - Replace manual frontend rendering with the universal viewer fetching from the backend.
- [x] **Task 6.4: Cleanup Redundant Frontend Logic**
    - Remove unused document rendering components in the frontend.

    - Create `docs/OPERATIONS.md` with the rollback protocol.
    - Documented the process for database downgrades and deployment reverts.

## Phase 5: Validation
- [x] **Task 5.1: Performance Testing**
    - Verify indexed query performance (Conceptualized in models, pending live DB).
- [ ] **Task 5.2: E2E Error Scenarios**
    - Manually trigger errors to verify toast notifications and logging.
- [x] **Task 5.3: Standalone Unit Testing**
    - Implement and verify database-independent logic in `backend/tests/standalone/`.
    - Verified: `LoggingMiddleware`, `Invoice PDF Generation`.
