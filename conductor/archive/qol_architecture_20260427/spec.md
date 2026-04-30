# Specification: Document Generation & QoL Hardening

## 1. Goal
Refine the application architecture to support a document-centric workflow (Risk Notes, Invoices, Renewals) and implement essential Quality of Life (QoL) features for production readiness.

## 2. Document Generation Architecture
- **Centralized Service:** Consolidate document generation logic in `backend/app/services/document.py`.
- **Entity Coverage:** 
    - **Risk Notes:** (Done) Atomic snapshots of coverage.
    - **Invoices:** (New) Financial snapshots linked to Risk Notes.
    - **Renewal Invitations:** (New) Prospective snapshots based on existing policies.
- **Storage:** Use a polymorphic `Document` model to track generated PDFs.

## 3. Database Indexing
- **Audit:** Identify slow queries in `Policy`, `RiskNote`, and `Invoice` tables.
- **Improvements:**
    - Composite indices for frequent filters (e.g., `client_id` + `status`).
    - GIN indices for JSON fields if they are frequently searched (e.g., `risk_details`).

## 4. Logging & Monitoring
- **Backend:** 
    - Implement a FastAPI middleware to log request metadata (method, path, status code, duration).
    - Use structured logging (JSON) for production compatibility.
- **Frontend:**
    - Capture and log frontend errors to the console in dev, and potentially an external service in prod.

## 5. Frontend Error Handling & Alerts
- **Global Error Boundary:** Wrap the main app to catch unhandled React errors.
- **TanStack Query Integration:** Use global `QueryClient` defaults to trigger toast alerts on API failures.
- **User Feedback:** Ensure all destructive actions (Delete, Cancel) have confirmation dialogs and success/error feedback.

## 6. Rollback Plan
- **Database:** Standardize Alembic `downgrade` scripts for every `upgrade`.
- **Deployment:** Document the process for reverting to a previous Docker image or Git tag.

## 7. Success Criteria
- Invoices can be generated as PDFs.
- All API errors result in a user-visible toast notification.
- Request logs are visible in the backend console.
- Database queries for common views (Policy list, Client history) are optimized with indices.
