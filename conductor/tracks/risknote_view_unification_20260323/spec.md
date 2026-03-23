# Specification: Risk Note View Unification & Fix

## 1. Overview
This track aims to resolve the misalignment between the digital Risk Note view and the generated PDF, as well as fix a critical bug causing the PDF view to hang infinitely. The strategic goal is to unify the rendering logic by using the backend-generated HTML as the single source of truth for both the PDF and the digital view in the frontend.

## 2. Functional Requirements
- **Unified Rendering:** The frontend "Digital View" must render the exact same HTML content that is used to generate the PDF. This replaces the current divergent React component implementation.
- **PDF Loading Fix:** The infinite loading issue in the PDF viewer must be diagnosed and resolved.
- **Interactive Experience:** The digital view (now HTML-based) should still feel integrated, potentially using an iframe or safe HTML injection, while maintaining the "Modern and Minimal" design aesthetic.

## 3. Technical Strategy (Unified HTML Source)
- **Backend:** Expose an endpoint (or update existing) to return the raw HTML content of the Risk Note (in addition to the PDF binary).
- **Frontend:** Refactor the Risk Note display component to fetch and render this HTML.
- **Bug Fix:** Investigate the `BlobPDFViewer` or equivalent component handling the PDF stream for the infinite loading cause.

## 4. Acceptance Criteria
- [ ] The "Digital View" of a Risk Note displays identical content and layout to the "PDF View".
- [ ] The PDF view loads correctly without hanging.
- [ ] Both views source data from the same backend template engine.
- [ ] Existing tests are updated to verify the new HTML serving endpoint and frontend integration.

## 5. Out of Scope
- Major redesign of the Risk Note template itself (we are aligning the views to the *current* template).
- Changes to the PDF generation library (WeasyPrint).
