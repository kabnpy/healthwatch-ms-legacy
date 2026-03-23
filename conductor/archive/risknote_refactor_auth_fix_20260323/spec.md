# Specification: Risk Note Template Refactor & Auth Fix

## 1. Overview
This track aims to simplify and harden the Risk Note generation process by transitioning to static, class-specific templates and fixing an authentication issue in the document endpoint. The primary focus is on the "Motor Private" insurance class, using a pre-defined layout for the financial breakdown while maintaining the existing letterhead.

## 2. Functional Requirements
- **Static Template Engine:**
  - Implement a template selection mechanism based on the policy's insurance class.
  - Create `motor_private.html` in the backend templates directory.
  - Hardcode specific clause information directly into the insurance class templates, removing the dependency on database-stored clauses.
  - Ensure the table layout and styling for "Motor Private" matches `planning/motor_private-risknote-template.html`.
  - Maintain the current project letterhead and footer in all generated PDFs.
- **Dynamic Data Injection:**
  - Use Jinja2 placeholders to inject dynamic data (Client Details, Vehicle/Risk Details, Premium Calculations) into the static templates.
  - Data retrieval must remain focused on existing models without requiring schema changes.
- **Authentication Fix:**
  - Investigate and resolve the authentication error (HTTP 401/403) occurring when accessing the document generation or retrieval endpoints.
  - Ensure standard `SessionDep` and `current_user` dependencies are correctly applied and validated.

## 3. Non-Functional Requirements
- **Maintainability:** Decoupling template layout from database state to reduce operational complexity.
- **Precision:** All financial figures must continue to use `Decimal` precision during injection.
- **Fidelity:** PDF output via WeasyPrint must match the approved HTML layout exactly.

## 4. Acceptance Criteria
- [ ] Document endpoint returns success (200 OK) for authenticated users.
- [ ] Risk Note PDF for "Motor Private" follows the static layout in `motor_private.html`.
- [ ] Clauses are visible in the PDF without being queried from the database.
- [ ] Dynamic data (client name, vehicle reg, net premium, etc.) is correctly rendered.
- [ ] Letterhead remains consistent with previous versions.

## 5. Out of Scope
- Modification of database models or migration scripts.
- Creation of templates for insurance classes other than "Motor Private" (to be handled in future tracks if needed).
