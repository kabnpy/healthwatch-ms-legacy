# Financials Implementation Strategy - Payments & Invoicing

## Objective
Implement a robust frontend system for managing Invoices, Receipts, and Allocations.

## 1. Route Structure
- `/financials`: Global view for accountants.
    - Tabs: `Invoices`, `Receipts`, `Overdue`.
- `/clients/$id/invoices`: Client-specific financial history and payment logging.

## 2. Data Fetching (hooks/useFinancials.ts)
- `useInvoices(params)`: Fetch all or client-specific invoices.
- `useReceipts(params)`: Fetch all or client-specific receipts.
- `useCreateReceipt()`: Mutation for logging new payments.
- `useAllocateReceipt()`: Mutation for linking receipts to invoices.

## 3. UI Components (components/Financials/)
- `InvoicesTable`: List invoices with status badges and "Allocate" actions.
- `ReceiptsTable`: List received payments.
- `AddReceiptForm`: Dialog for logging new money.
- `AllocationDialog`: The "bridge" UI to distribute receipt amounts to invoices.

## 4. Business Rules (Frontend)
- A Receipt cannot be allocated for more than its total amount.
- An Invoice status is derived from `total_amount - allocated_amount`.
- Voiding a receipt reverses all associated allocations and restores invoice balances.

## 5. Audit & Visibility
- [x] **Allocation History:** View which receipts paid an invoice (and vice versa).
- [x] **Printable Receipts:** Official receipt template in the document viewer.
- [x] **Global Search:** Find invoices/receipts by number via Ctrl+K.
- [x] **Overview Integration:** Outstanding balance visible on Client Dashboard.

## Progress
- [x] Global Route `/financials` (Deferred - Analytics needed)
- [x] `useFinancials` hook (Full CRUD + Voiding)
- [x] Receipts Table (With balance tracking)
- [x] Add Receipt Form
- [x] Allocation UI (With live balance validation)
- [x] Client Hub Integration (History, Voiding, Printing)
- [ ] Final Verification (Build/Lint/Reversal Test)
