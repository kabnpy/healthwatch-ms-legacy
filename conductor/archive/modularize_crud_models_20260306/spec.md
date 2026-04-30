# Specification: Refactor CRUD and Models into Modules

## 1. Overview
The current implementation of `backend/app/models.py` and `backend/app/crud.py` has become monolithic and difficult to maintain as the project grows. This track aims to refactor these two files into domain-specific modules for better organization, improved readability, and easier maintenance.

## 2. Functional Requirements
- **Models Refactoring:**
  - Break down `backend/app/models.py` into domain-specific modules under a new `backend/app/models/` directory.
  - Domains to include:
    - **Clients:** `client.py` (Client models, KYC documents).
    - **Policies:** `policy.py` (Policy, RiskNote, and financial logic within Policy).
    - **Claims:** `claim.py` (Claim tracking models).
    - **Auth/User:** `user.py` (User, Item, and other template-related models).
    - **Shared/Audit:** `audit.py` (Common audit fields like `created_at`, `updated_at`, etc.).
  - Implement unified exports in `backend/app/models/__init__.py`.

- **CRUD Refactoring:**
  - Break down `backend/app/crud.py` into domain-specific modules under a new `backend/app/crud/` directory.
  - Domains to match models:
    - `client.py`
    - `policy.py`
    - `claim.py`
    - `user.py`
  - Implement unified exports in `backend/app/crud/__init__.py`.

- **Dependency Management:**
  - Ensure all internal imports across the codebase are updated to reflect the new structure.
  - Proactively identify and resolve potential circular dependencies during the refactoring process.

## 3. Non-Functional Requirements
- **Consistency:** Maintain existing naming conventions and coding styles. Use singular names for files (e.g., `client.py`).
- **Data Integrity:** The refactoring must not alter any existing database schemas or logic.
- **Maintainability:** Ensure the new structure is intuitive for future development and testing.

## 4. Acceptance Criteria
- [ ] `backend/app/models.py` and `backend/app/crud.py` are successfully removed or emptied in favor of the new modular structure.
- [ ] All existing tests pass without modification or with minimal import-related adjustments.
- [ ] No new circular dependencies are introduced.
- [ ] The application remains fully functional across all existing features (Clients, Policies, Claims, Auth).
- [ ] Unified exports allow existing imports from `app.models` and `app.crud` to continue working where possible, or all import sites are updated.

## 5. Out of Scope
- Any changes to database schemas or migrations (unless absolutely necessary for refactoring).
- Introduction of new features or business logic.
- Separation of financial logic into a standalone module (requested to keep within Policies).
