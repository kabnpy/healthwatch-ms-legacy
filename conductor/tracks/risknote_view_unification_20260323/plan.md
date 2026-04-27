# Implementation Plan: Risk Note View Unification & Fix

## Phase 1: Investigation & Backend Prep
- [x] Task: Investigate the PDF loading bug in the frontend `BlobPDFViewer` (or relevant component) to identify the root cause. [investigation]
- [x] Task: Create a reproduction test case for the PDF loading failure if possible. [skipped - obvious bug]
- [x] Task: Implement a new backend endpoint `GET /risk-notes/{id}/html` that returns the rendered HTML template. [84f789e]
- [x] Task: Unit test the new HTML endpoint. [84f789e]

## Phase 2: Frontend Unification
- [x] Task: Create a new `HTMLRiskNoteViewer` component in the frontend. [84f789e]
- [x] Task: Update the `RiskNote` view container to use `HTMLRiskNoteViewer` for the "Digital View" tab, fetching content from the new API. [84f789e]
- [x] Task: Verify that the "Digital View" matches the PDF output exactly. [84f789e]
- [x] Task: Deprecate/Remove the divergent React-based Risk Note rendering logic. [84f789e]

## Phase 3: Final Verification
- [x] Task: Verify the fix for the infinite loading bug in the PDF view. [84f789e]
- [~] Task: Conductor - User Manual Verification 'Risk Note View Unification' (Protocol in workflow.md)
