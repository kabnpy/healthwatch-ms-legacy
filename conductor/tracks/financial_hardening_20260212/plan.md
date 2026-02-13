# Implementation Plan: Core Financial and Architectural Hardening

This plan outlines the steps to implement financial precision, architectural separation, and security hardening as specified in `spec.md`.

## Phase 1: Foundation and Financial Precision
- [x] Task: Migrate money fields to Decimal [1801145]
    - [ ] Write Tests: Verify floating point errors in existing models
    - [ ] Implement: Update models (Policy, Invoice, Receipt, RiskNote) to use Decimal and Numeric(15, 2)
    - [ ] Implement: Update all dependent calculations and seed data
- [x] Task: Implement Soft Delete and Audit Trail [bda61e6]
    - [ ] Write Tests: Verify soft delete behavior and audit metadata
    - [ ] Implement: Create AuditMixin and apply to primary models
    - [ ] Implement: Update CRUD to respect deleted_at flag
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Foundation' (Protocol in workflow.md)

## Phase 2: Security and Type Safety
- [ ] Task: Replace Status Strings with Enums
    - [ ] Write Tests: Verify enum validation in models
    - [ ] Implement: Create Enums for all entity statuses
    - [ ] Implement: Update models and migrations
- [ ] Task: Implement Role-Based Access Control (RBAC)
    - [ ] Write Tests: Verify access denial for VIEWER on mutation routes
    - [ ] Implement: Create @require_role decorator
    - [ ] Implement: Apply to API endpoints
- [ ] Task: Add Database Indexes for Foreign Keys
    - [ ] Implement: Add indexes to all FKs in models and generate migrations
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Security' (Protocol in workflow.md)

## Phase 3: Architectural Separation
- [ ] Task: Establish Service Layer
    - [ ] Implement: Create `backend/app/services/` directory
    - [ ] Implement: Move Risk Note + Invoice atomic logic to PolicyService
- [ ] Task: Refactor Document Model with PostgreSQL Inheritance
    - [ ] Write Tests: Verify referential integrity and polymorphic behavior
    - [ ] Implement: Create new document hierarchy
- [ ] Task: Implement Motor Private Schema Validation
    - [ ] Write Tests: Verify validation of Motor Private risk_details
    - [ ] Implement: Create Pydantic schema for vehicle details
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Architecture' (Protocol in workflow.md)
