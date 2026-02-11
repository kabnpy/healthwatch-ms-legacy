# Strategy: Simplified Insurance Models

## Goal
Simplify the data architecture by removing redundant layers (`RiskItem`) and merging cover-specific details directly into the `Policy` model. 1 Policy = 1 Cover Instance.

## 1. Entity Definitions (Refined)

### A. Product (The Class/Template)
- **Role**: Defines what a type of insurance looks like (generic).
- **Location**: `backend/app/models/insurance/catalog.py`
- **Fields**: Insurer, Name, Class of Insurance, Form Schema (for dynamic wizards).

### B. Policy (The Instance/Cover)
- **Role**: A specific cover taken by a client. This is the "Instance" of a Product.
- **Location**: `backend/app/models/insurance/policy.py`
- **Fields (Core)**:
    - `policy_number`: The insurer's reference number.
    - `client_id`: Link to Client.
    - `product_id`: Link to Product (The Class).
    - `status`: Active, Lapsed, etc.
- **Fields (Cover Details)**:
    - `start_date`, `end_date`: Period of insurance.
    - `description`: Human-readable summary (e.g., "Motor Private - KCA 123B").
    - `total_premium`: Annual premium (including all taxes/levies).
    - `premium_breakdown`: JSON (Details of levies, taxes, basic premium).
    - `risk_details`: JSON (Class-specific values like Vehicle Reg, Sum Insured, etc.).

### C. Risk Note (The Transaction/Document)
- **Role**: A snapshot of the Policy at a specific point in time (New Business, Renewal, Endorsement).
- **Location**: `backend/app/models/insurance/policy.py`
- **Fields**:
    - `policy_id`: Link to Policy.
    - `transaction_type`: New Business, Renewal, etc.
    - `policy_snapshot`: JSON (Frozen state of the Policy's cover details).
    - Financial aggregates for the specific transaction.

### D. Financials (Invoices & Receipts)
- **Invoice**: Links to `RiskNote`.
- **Receipt**: Reconciliation of payments received from insurance companies or clients.

---

## 2. Measurable Steps

### Phase 1: Model Review & Schema Update
- [x] **Step 1.1**: Update `Policy` model to include fields previously in `RiskItem`.
- [x] **Step 1.2**: Update `RiskNote` to snapshot the `Policy` fields instead of `RiskItem`.
- [x] **Step 1.3**: Deprecate `RiskItem` model and relationships.

### Phase 2: Data Migration
- [x] **Step 2.1**: Create a migration script to move existing data from `RiskItem` to `Policy`.
- [x] **Step 2.2**: Ensure `items_snapshot` in `RiskNote` is compatible with the new structure.

### Phase 3: Backend Refactoring (CRUD & API)
- [x] **Step 3.1**: Update `Policy` CRUD to handle `risk_details` and `premium_breakdown`.
- [x] **Step 3.2**: Update `RiskNote` generation logic to pull from `Policy`.
- [x] **Step 3.3**: Update API endpoints and Public schemas.

### Phase 4: Frontend Refactoring (Wizards & Views)
- [x] **Step 4.1**: Update "New Policy" Wizard to save directly to `Policy` (removing the `RiskItem` step).
- [x] **Step 4.2**: Update "Insurance Dashboard" to display `Policy` details directly.
- [x] **Step 4.3**: Update "Risk Note Viewer" to use the new snapshot structure.

### Phase 5: Verification & Cleanup
- [x] **Step 5.1**: Verify PDF/HTML generation for Risk Notes and Invoices.
- [x] **Step 5.2**: Final removal of `RiskItem` code and database table.

### Phase 6: Type Integrity & Build Stabilization
- [ ] **Step 6.1**: Regenerate `openapi.json` ensuring no `RiskItem` schemas or endpoints exist.
- [ ] **Step 6.2**: Cleanly regenerate the frontend client (`rm -rf src/client`).
- [ ] **Step 6.3**: Fix persistent TypeScript errors in `DocumentViewer.tsx`, `RiskNoteForm.tsx`, and `NewPolicyWizard.tsx` caused by stale type definitions.
- [ ] **Step 6.4**: Achieve a clean `npm run build`.

---

## 3. Branching Strategy
- Work on a new branch `refactor/simplified-models`.
- If possible, base it on a commit where document generation was stable (e.g., `6aed7ec` or the latest `main`).
