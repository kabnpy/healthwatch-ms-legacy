# Backend Data Models (Refined Architecture)

> **STATUS:** FINAL
> **CONTEXT:** Supports "Time Travel" (History), Cashiering, and Polymorphic File Storage.

---

## 1. CORE ENTITIES (Identity)

### `User`
*The staff members accessing the system.*
- `id`: UUID (Primary Key).
- `email`: String (Unique).
- `full_name`: String.
- `role`: Enum (`Admin`, `Underwriter`, `Cashier`, `Viewer`).
- `is_active`: Boolean.

### `Client`
*The customer.*
- `id`: UUID.
- `name`: String (Individual or Corporate Name).
- `kra_pin`: String (Tax ID - Critical for Invoicing).
- `email`: String.
- `phone`: String.
- `physical_address`: Text.

---

## 2. POLICY ENGINE (The Transaction Log)

### `Policy`
*The container for coverage. It represents the "Folder".*
- `id`: UUID.
- `client_id`: FK -> Client.
- `product_id`: FK -> Product (e.g., "Motor Private").
- `policy_number`: String (Unique, e.g., "P/001/2026").
- `status`: Enum (`Active`, `Lapsed`, `Cancelled`).
- `created_at`: Timestamp.

### `RiskItem` (The Asset)
*Implements **Temporal Versioning**. We never update in place; we expire and create new.*
- `id`: UUID.
- `policy_id`: FK -> Policy.
- **`version_number`**: Int (Increments: 1, 2, 3...).
- **`valid_from`**: Date (Start of this specific version).
- **`valid_to`**: Date (Nullable. None = Currently Active).
- `is_active`: Boolean (Helper field for queries).
- `identifier`: String (e.g., Vehicle Reg No).
- `description`: String (e.g., "Toyota Harrier").
- `sum_insured`: Decimal.
- `details`: JSON (Flexible bucket for "Chassis No", "Engine No", "Color").

### `RiskNote` (The Transaction & Invoice)
*Dual purpose: Legal Certificate + Financial Debit Note.*
- `id`: UUID.
- `policy_id`: FK -> Policy.
- **`transaction_type`**: Enum (`New Business`, `Renewal`, `Endorsement`, `Cancellation`).
- **`previous_risk_note_id`**: FK -> RiskNote (Self-referential history chain).
- `risk_note_number`: String (Internal Ref).
- **`invoice_number`**: String (Official Tax Invoice #).
- **`created_by_id`**: FK -> User (For "Prepared By" audit trail).
- `start_date`: Date (Cover start).
- `end_date`: Date (Cover end).
- `basic_premium`: Decimal.
- `taxes_and_levies`: JSON (Breakdown of Stamp Duty, Training Levy, etc.).
- `gross_premium`: Decimal (Total Payable).
- `payment_status`: Enum (`Unpaid`, `Partial`, `Paid`).

---

## 3. FINANCIALS (Cashiering)

### `Payment` (Money In)
*Represents a raw inflow of funds (Check, M-Pesa, etc).*
- `id`: UUID.
- `date`: Date.
- `amount`: Decimal (Total received).
- **`unallocated_amount`**: Decimal (Ideally equals `amount` initially. Drops to 0 as it is used).
- `payment_mode`: Enum (`Cheque`, `MPESA`, `BankTransfer`, `Cash`).
- `reference`: String (Transaction Code).
- `created_by_id`: FK -> User.

### `PaymentAllocation` (The Link)
*Mapping money from a Payment to a specific Debt (Risk Note).*
- `id`: UUID.
- `payment_id`: FK -> Payment.
- `risk_note_id`: FK -> RiskNote.
- `amount_allocated`: Decimal.
- `created_at`: Timestamp.

---

## 4. CLAIMS (Triage)

### `Claim`
*The header for a loss incident.*
- `id`: UUID.
- `policy_id`: FK -> Policy.
- **`risk_item_id`**: FK -> RiskItem (Links to the specific version of the car at time of loss).
- `claim_number`: String.
- `date_of_loss`: Date.
- `date_reported`: Date.
- `status`: Enum (`Reported`, `Under Investigation`, `Approved`, `Declined`, `Paid`).
- `reserve_amount`: Decimal (Estimated liability).

### `ClaimEvent`
*The timeline of actions taken on a claim.*
- `id`: UUID.
- `claim_id`: FK -> Claim.
- `event_type`: Enum (`Notification`, `Assessment`, `Correspondence`, `Payment`).
- `description`: Text.
- `created_by_id`: FK -> User.
- `created_at`: Timestamp.

---

## 5. DOCUMENTS (The Vault)

### `Document` (Polymorphic)
*A single table for all file attachments across the system.*
- `id`: UUID.
- **`entity_type`**: Enum (`Client`, `Policy`, `Claim`, `User`).
- **`entity_id`**: UUID (The ID of the Client/Policy/Claim).
- `document_type`: Enum (`Logbook`, `ID`, `Valuation`, `PoliceAbstract`, `Receipt`).
- `file_path`: String (Local path or S3 Key).
- `mime_type`: String.
- `uploaded_at`: Timestamp.
