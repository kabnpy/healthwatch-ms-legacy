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
- An Invoice status should be derived from `total_amount - allocated_amount`.
- "Partial" status occurs if `allocated_amount > 0` but `< total_amount`.

## Progress
- [ ] Global Route `/financials`
- [ ] `useFinancials` hook
- [ ] Receipts Table
- [ ] Add Receipt Form
- [ ] Allocation UI
- [ ] Client Hub Integration
