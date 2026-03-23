# Implementation Plan: Risk Note Template Refactor & Auth Fix

## Phase 1: Diagnosis & Authentication Fix
- [x] Task: Investigate `backend/app/api/routes/documents.py` for authentication inconsistencies. [1e6629e]
- [x] Task: Create a reproduction test case that fails when accessing document endpoints without proper headers or with correct ones. [1e6629e]
- [x] Task: Fix the authentication dependency in `backend/app/api/routes/documents.py` if needed (ensure `SecurityDep` is properly handled). [1e6629e]

## Phase 2: Template Selection Refactor
- [x] Task: Modify `backend/app/services/document_service.py` to support class-specific templates. [1e6629e]
- [x] Task: Create `backend/app/templates/documents/motor_private.html` extending `documents/base.html`. [1e6629e]

## Phase 3: Motor Private Template Implementation
- [x] Task: Implement the table structure from `planning/motor_private-risknote-template.html` into `motor_private.html`. [1e6629e]
- [x] Task: Hardcode the static clauses (Benefits, Excess, Special Clauses) directly into `motor_private.html`. [1e6629e]
- [x] Task: Add Jinja2 placeholders for dynamic data: [1e6629e]
    - Client name, PIN, Address.
    - Policy Number.
    - Period (Start/End).
    - Vehicle Details (Reg No, Make, Year, Value).
    - Premium Breakdown (Net Premium, Taxes, Levies, Total).
    - Insurer Name.

## Phase 4: Verification & Cleanup
- [x] Task: Verify PDF generation for a Motor Private policy. [1e6629e]
- [x] Task: Verify that the authentication fix allows the frontend to retrieve/generate documents correctly. [1e6629e]
- [x] Task: Conductor - User Manual Verification 'Risk Note Template Refactor' (Protocol in workflow.md) [1e6629e]
