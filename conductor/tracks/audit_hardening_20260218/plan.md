# Implementation Plan: Product Versioning & Audit Hardening

This plan details the implementation of explicit product versioning, normalized client contacts, and system-wide audit trail enforcement to ensure long-term data integrity and auditability.

## Phase 1: Product Versioning & Immutability [checkpoint: ]
Implement the logic to version products instead of mutating them.

- [ ] Task: Create a new feature branch `feat/audit-hardening`.
- [ ] Task: **Update Product Model**: Add `version`, `is_active`, and `superseded_by_id` fields in `backend/app/models.py`.
- [ ] Task: Generate and verify Alembic migration for Product versioning.
- [ ] Task: **Write Tests for Versioning**: Create unit tests that verify creating a "new version" of a product preserves the old one.
- [ ] Task: Refactor `Product` CRUD to handle the "version on update" logic.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Product Versioning & Immutability' (Protocol in workflow.md)

## Phase 2: Client Contact Normalization [checkpoint: ]
Move contact details from JSON to a dedicated relational table.

- [ ] Task: **Create ClientContact Model**: Implement the new table in `backend/app/models.py` with proper foreign keys and indexes.
- [ ] Task: **Data Migration**: Create an Alembic script to move existing `Client.contacts` JSON data into the `ClientContact` table.
- [ ] Task: Update Client schemas and CRUD to manage the new relationship.
- [ ] Task: Refactor Frontend Client Form to interact with the new relational contact structure.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Client Contact Normalization' (Protocol in workflow.md)

## Phase 3: Global Audit Reinforcement [checkpoint: ]
Ensure all core entities correctly track metadata and soft deletes.

- [ ] Task: Audit all core models (`Client`, `Product`, `Policy`, `RiskNote`, `Invoice`) for `AuditMixin` consistency.
- [ ] Task: Generate a final "Cleanup" migration to add any missing audit or soft-delete columns.
- [ ] Task: **Verify Auth Triggers**: Ensure `created_by_id` is automatically set for all entities during creation.
- [ ] Task: Update the `Soft Delete` test suite to cover the new tables.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Global Audit Reinforcement' (Protocol in workflow.md)

## Phase 4: Integration & Final Verification [checkpoint: ]
Validate historical integrity across the stack.

- [ ] Task: Regenerate frontend API client (`npm run generate-client`).
- [ ] Task: Verify that historical Policy views correctly display the terms from their specific Product Version.
- [ ] Task: **Verify Coverage**: Ensure >80% coverage for the new versioning and contact logic.
- [ ] Task: Execute final build check and linting.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Integration & Final Verification' (Protocol in workflow.md)
