# Implementation Plan: Risk Note View Unification & Fix

## Phase 1: Investigation & Backend Prep
- [ ] Task: Investigate the PDF loading bug in the frontend `BlobPDFViewer` (or relevant component) to identify the root cause.
- [ ] Task: Create a reproduction test case for the PDF loading failure if possible.
- [ ] Task: Implement a new backend endpoint `GET /risk-notes/{id}/html` that returns the rendered HTML template.
- [ ] Task: Unit test the new HTML endpoint.

## Phase 2: Frontend Unification
- [ ] Task: Create a new `HTMLRiskNoteViewer` component in the frontend.
- [ ] Task: Update the `RiskNote` view container to use `HTMLRiskNoteViewer` for the "Digital View" tab, fetching content from the new API.
- [ ] Task: Verify that the "Digital View" matches the PDF output exactly.
- [ ] Task: Deprecate/Remove the divergent React-based Risk Note rendering logic.

## Phase 3: Final Verification
- [ ] Task: Verify the fix for the infinite loading bug in the PDF view.
- [ ] Task: Conductor - User Manual Verification 'Risk Note View Unification' (Protocol in workflow.md)
