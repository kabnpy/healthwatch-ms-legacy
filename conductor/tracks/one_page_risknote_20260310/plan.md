# Implementation Plan: One-page A4 Risk Note PDF Generation

## Phase 0: Setup & Branching
- [x] Task: Create a new git branch for the track: `feat/one-page-risknote`. 23fdb0e
- [ ] Task: Conductor - User Manual Verification 'Phase 0' (Protocol in workflow.md)

## Phase 1: Setup & Tooling Selection
- [ ] Task: Evaluate and install HTML-to-PDF library (e.g., WeasyPrint or Playwright).
- [ ] Task: Create a base PDF layout template with A4 dimensions and standard print margins.
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: HTML/CSS Template Design
- [ ] Task: Implement multi-column CSS layout for Policy Terms and Coverage Details.
- [ ] Task: Develop the Jinja2 template for the Risk Note PDF incorporating agency branding.
- [ ] Task: Implement dynamic CSS rules for font-scaling and line-height optimization for dense data.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Backend PDF Generation Service
- [ ] Task: Create a Python service in `backend/app/services/document_service.py` for PDF generation.
- [ ] Task: Write failing unit tests for the PDF generation service (Red Phase).
- [ ] Task: Implement the PDF service to pass tests using the selected library (Green Phase).
- [ ] Task: Integrate the PDF service with the Risk Note creation endpoint to generate and store/serve the PDF.
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Validation & Merge
- [ ] Task: Perform "Stress Test" with various data volumes to verify the single-page constraint.
- [ ] Task: Finalize the branch and prepare for merge into `main`.
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)