# Specification: Product Versioning & Audit Hardening

## 1. Overview
This track focuses on making the system "Audit-Ready" by ensuring that changes to product templates do not corrupt historical data and that all primary entity mutations are fully tracked. It implements explicit versioning for Products and normalizes Client Contact data for granular auditing.

## 2. Functional Requirements

### 2.1 Explicit Product Versioning
- **Versioning Logic:** Add `version` (int), `is_active` (bool), and `superseded_by_id` (UUID) to the `Product` model.
- **Immutability Principle:** Once a Product version is used in an issued Risk Note, it cannot be edited. Any changes to rates or terms must result in a new Product version.
- **UI Logic:** The "New Policy Wizard" will only show `is_active=True` products, but historical dashboards will correctly display the name and terms of the specific version used.

### 2.2 Client Contact Normalization
- **New Entity:** Create a `ClientContact` model/table.
- **Attributes:** `id`, `client_id`, `contact_type` (Primary, Billing, etc.), `name`, `email`, `phone`.
- **Migration:** Move existing data from the `Client.contacts` JSON field into the new table and then remove the JSON field.

### 2.3 System-Wide Audit Hardening
- **AuditMixin Enforcement:** Ensure `AuditMixin` is implemented on:
    - `Client`
    - `Product`
    - `Policy`
    - `RiskNote`
    - `Invoice`
- **Audit Triggers:** Verify that `created_by_id` and `updated_at` are correctly populated via backend dependency injection (`CurrentUser`).

## 3. Non-Functional Requirements
- **Data Integrity:** Historical policies must be retrievable even if their parent product has been "updated" (versioned).
- **Query Performance:** Ensure indexes exist on `is_active` and `client_id` in the normalized contact table.

## 4. Acceptance Criteria
- [ ] Changing a Product's details via the API creates a new record with an incremented version number.
- [ ] Existing policies remain linked to their original Product version.
- [ ] Client contacts are managed in a separate table with individual audit timestamps.
- [ ] All primary tables contain `created_at`, `updated_at`, and `deleted_at` columns.

## 5. Out of Scope
- Full Bitemporal "As-of" queries (tracking valid timeline vs recording timeline).
- Reverting to previous product versions via the UI.
