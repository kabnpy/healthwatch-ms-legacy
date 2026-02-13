# Specification: Transactional RiskNote Architectural Refactor

## 1. Overview
This track involves refactoring the core insurance models and business logic to implement the "Transactional RiskNote" pattern. The goal is to establish the `RiskNote` as the single source of truth for all policy states (coverage details, premiums, and terms), while the `Policy` entity becomes a lightweight container for metadata and relationships.

## 2. Functional Requirements

### 2.1 Backend Refinement
- **Model Updates (`backend/app/models/`)**:
    - Remove coverage-specific fields from the `Policy` model (e.g., `risk_details`, `total_premium`, `premium_breakdown`, `start_date`, `end_date`).
    - Implement computed properties (or API response decorators) on the `Policy` model to retrieve the "current state" from the latest associated `RiskNote`.
    - Ensure `RiskNote.policy_snapshot` is a complete, frozen representation of the policy and product at the time of issuance.
- **CRUD & Service Layer Refactoring**:
    - Refactor `PolicyService.create_policy` to ensure it only initializes the container and immediately creates the first `RiskNote` (New Business).
    - Update all logic that currently modifies `Policy.risk_details` to instead generate a new `RiskNote` (Endorsement/Renewal).
    - Ensure the "Simplified RBAC" is maintained during these new mutation flows.

### 2.2 Frontend Refinement
- **Data Retrieval**:
    - Update policy-related components (Dashboard, Details view) to fetch and display data from the latest `RiskNote` via the API.
    - Update the "New Policy Wizard" to handle the two-step creation (Policy container + initial Risk Note) atomically.
- **UI Consistency**:
    - Ensure that history views correctly pull from past `RiskNote` snapshots to show the evolution of the policy.

### 2.3 Data & Testing
- **Database Reset**: Perform a destructive reset of the local database to apply the new schema.
- **Seed Script (`backend/app/seed_mock_data.py`)**: Rewrite the mock data generation to strictly follow the new transactional pattern.
- **Test Suite**: Update existing unit and integration tests to validate the new architectural flow.

## 3. Non-Functional Requirements
- **Data Integrity**: Eliminate all data duplication between the `Policy` and `RiskNote` tables.
- **Performance**: Optimize the "latest RiskNote" query using composite indexes as specified in the data modeling document.
- **Architectural Rigor**: Maintain strictly immutable `RiskNote` records once their status is changed from 'Draft'.

## 4. Acceptance Criteria
- [ ] The `Policy` database table no longer contains duplicated coverage or premium fields.
- [ ] Creating a new policy successfully generates both a `Policy` record and an initial `RiskNote`.
- [ ] Updating a policy's details generates a new `RiskNote` without modifying the `Policy` table's coverage metadata.
- [ ] The frontend accurately displays current policy details by reading from the latest `RiskNote`.
- [ ] The `seed_mock_data.py` script runs without errors and correctly populates the new structure.

## 5. Out of Scope
- Implementing the user interface for complex Endorsements (this track focuses on the architectural refactor).
- Changes to the Financial/Invoicing logic beyond ensuring they point to the correct `RiskNote` source.
