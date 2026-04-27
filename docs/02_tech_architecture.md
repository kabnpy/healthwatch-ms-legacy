# Technical Architecture

## 1. Tech Stack
- **Frontend:** React (Vite), TanStack Query, TanStack Router, Shadcn UI, Tailwind CSS.
- **Backend:** Python (FastAPI), SQLModel (SQLAlchemy + Pydantic).
- **Database:** PostgreSQL (Managed via Neon.tech).
- **Runtime:** `uv` (Local Python management), Docker (Production Container).
- **Client Gen:** `openapi-generator` (Syncs Frontend types with Backend).

## 2. Database Schema Strategy
We use a **Transaction Log** approach for Risk Notes and a **Temporal Versioning** approach for Risk Items to support "Time Travel" (Endorsements) without losing history.

### Key Models
- **RiskNote (The Transaction):**
  - `transaction_type`: Enum (`New Business`, `Renewal`, `Endorsement`, `Cancellation`).
  - `invoice_number`: Optional[str] (For tax compliance/eTIMS).
  - `previous_risk_note_id`: FK (Self-referential link to history).
  - `payment_status`: Enum (`Unpaid`, `Partial`, `Paid`).
- **RiskItem (The Asset History):**
  - `valid_from`: Date.
  - `valid_to`: Date (Nullable).
  - `version_number`: Int (Increments on change).
  - `is_active`: Bool.
  - *Logic:* We never update a Risk Item in place. We "expire" the old one (set `valid_to`) and create a new one with `version_number + 1`.

## 3. Deployment Architecture (Split-Stack)
- **Frontend:** Deployed to Vercel (Static Site).
- **Backend:** Deployed to Render (Python Native).
- **DB:** Managed Postgres on Neon.
- **Config:** Frontend consumes `VITE_API_URL` environment variable.

alternative railway.app single point for deployments

## 4. Feature Flagging Strategy
We use a local config file to manage complexity and gate incomplete features.
- **File:** `frontend/src/config/features.ts`
- **Mechanism:** Simple boolean export.
  ```typescript
  export const FEATURES = {
    NEW_BUSINESS: true,     // MVP
    DASHBOARD_VIEW: true,   // MVP
    PRINT_RISK_NOTE: true,  // MVP
    ENDORSEMENTS: false,    // Future (Requires Temporal Logic)
    RENEWALS: false,        // Future (Requires Batch Logic)
    CLAIMS: false           // Future (Requires Workflow Engine)
  };
  ```

## 5. Architectural Decisions
- **Atomic Snapshot Strategy**: The system stores the full state of a risk (the "Snapshot") on the `RiskNote` issued for each transaction. This ensures that every document (Risk Note, Invoice) refers to the authoritative state of the cover at the exact moment of issuance.
- **Policy as the Contract Container**: The `Policy` model remains the long-lived container for the contract, but coverage-specific data (dates, values) is derived from its related `RiskNotes`.
- **Hybrid Document Viewing**: We maintain both an interactive "Digital View" (for editing drafts) and a "PDF View" (for official documentation) within the frontend.

## 6. Future Optimizations
- **Policy Expiry Denormalization**: Consider denormalizing `current_coverage_end` onto the `Policy` model to improve query performance.
- **Reporting Engine**: Implement a consolidated reporting view using Materialized Views for complex financial aggregates.
