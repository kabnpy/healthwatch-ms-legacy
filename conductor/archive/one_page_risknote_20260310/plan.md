# Implementation Plan: One-page A4 Risk Note PDF Generation

## Phase 0: Setup & Branching [checkpoint: 3ca4147]
- [x] Task: Create a new git branch for the track: `feat/one-page-risknote`. 23fdb0e
- [x] Task: Conductor - User Manual Verification 'Phase 0' (Protocol in workflow.md) 3ca4147

## Phase 1: Setup & Tooling Selection [checkpoint: 3e95a72]
- [x] Task: Evaluate and install HTML-to-PDF library (e.g., WeasyPrint or Playwright). 550d3fc
- [x] Task: Create a base PDF layout template with A4 dimensions and standard print margins. 1e327e0
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md) 3e95a72

## Phase 2: HTML/CSS Template Design [checkpoint: 71e7ab6]
- [x] Task: Implement multi-column CSS layout for Policy Terms and Coverage Details. 6f6625d
- [x] Task: Develop the Jinja2 template for the Risk Note PDF incorporating agency branding. 6f6625d
- [x] Task: Implement dynamic CSS rules for font-scaling and line-height optimization for dense data. c8ea99f
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md) 71e7ab6

## Phase 3: Backend PDF Generation Service [checkpoint: 7711fd7]
- [x] Task: Create a Python service in `backend/app/services/document_service.py` for PDF generation. 7d8d1a1
- [x] Task: Write failing unit tests for the PDF generation service (Red Phase). 7d8d1a1
- [x] Task: Implement the PDF service to pass tests using the selected library (Green Phase). 7d8d1a1
- [x] Task: Integrate the PDF service with the Risk Note creation endpoint to generate and store/serve the PDF. 64197df
- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md) 7711fd7

## Phase 4: Validation & Merge [checkpoint: eec8fc3]
- [x] Task: Perform "Stress Test" with various data volumes to verify the single-page constraint. 24ad694
- [x] Task: Finalize the branch and prepare for merge into `main`. bc658e23
- [x] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md) eec8fc3

## Phase 5: Frontend Integration & Polish [checkpoint: ]
- [x] Task: Fix `displayName` regression in Policy Dashboard.
- [x] Task: Implement "Digital" vs "PDF" view toggle in Policy Overview.
- [x] Task: Add "PDF View" action to Transaction History table and timeline.
- [x] Task: Update `DocumentViewer` to support official PDF rendering via iframe.
- [x] Task: Implement `BlobPDFViewer` for authenticated PDF fetching.
- [x] Task: Implement `downloadAuthenticatedFile` for secure PDF downloads.
- [ ] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)