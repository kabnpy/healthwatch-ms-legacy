# Implementation Plan: Risk Note Template Refactor & Auth Fix

## Phase 1: Diagnosis & Authentication Fix
- [ ] Task: Investigate `backend/app/api/routes/documents.py` for authentication inconsistencies.
- [ ] Task: Create a reproduction test case that fails when accessing document endpoints without proper headers or with correct ones.
- [ ] Task: Fix the authentication dependency in `backend/app/api/routes/documents.py` if needed (ensure `SecurityDep` is properly handled).

## Phase 2: Template Selection Refactor
- [ ] Task: Modify `backend/app/services/document_service.py` to support class-specific templates.
    - Logic: Check `policy.product.class_of_insurance`.
    - If "Motor Private", use `documents/motor_private.html`.
    - Fallback to `documents/risknote.html`.
- [ ] Task: Create `backend/app/templates/documents/motor_private.html` extending `documents/base.html`.

## Phase 3: Motor Private Template Implementation
- [ ] Task: Implement the table structure from `planning/motor_private-risknote-template.html` into `motor_private.html`.
- [ ] Task: Hardcode the static clauses (Benefits, Excess, Special Clauses) directly into `motor_private.html`.
- [ ] Task: Add Jinja2 placeholders for dynamic data:
    - Client name, PIN, Address.
    - Policy Number.
    - Period (Start/End).
    - Vehicle Details (Reg No, Make, Year, Value).
    - Premium Breakdown (Net Premium, Taxes, Levies, Total).
    - Insurer Name.

## Phase 4: Verification & Cleanup
- [ ] Task: Verify PDF generation for a Motor Private policy.
- [ ] Task: Verify that the authentication fix allows the frontend to retrieve/generate documents correctly.
- [ ] Task: Conductor - User Manual Verification 'Risk Note Template Refactor' (Protocol in workflow.md)
