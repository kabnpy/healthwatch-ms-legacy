# Track: One-page A4 Risk Note PDF Generation

## 1. Overview
The goal of this track is to refine the generation of Risk Note PDF documents to ensure they consistently fit on a single A4 page. This will involve creating a highly optimized HTML/CSS layout that utilizes multi-columns and dynamic scaling to maintain legibility while accommodating varying amounts of policy data.

## 2. Functional Requirements
- **A4 PDF Generation:** Implement a service to convert HTML/CSS templates into PDF documents formatted for standard A4 paper (210mm x 297mm).
- **Single-Page Constraint:** The layout must be designed to fit all core Risk Note information (Client, Policy Details, Financial Breakdown, Terms) on one page for typical use cases.
- **Multi-Column Layout:** Use CSS (Grid/Flexbox) to display "Coverage Details" and "Policy Terms" in a multi-column format to maximize space.
- **Dynamic Styling:** Implement print-specific CSS to adjust font sizes and line spacing dynamically if the content exceeds the page height, down to a minimum legible font size (e.g., 9pt).
- **Standard Branding:** Include agency branding (logo, contact info) in a compact header/footer.

## 3. Technical Requirements
- **Library Selection:** Utilize a robust HTML-to-PDF library (e.g., `WeasyPrint` or a headless browser via `Playwright`) compatible with the Python/FastAPI backend.
- **CSS for Print:** Use `@media print` and CSSPagedMedia rules for precise margin control and layout.
- **Template Engine:** Leverage `Jinja2` (already standard in FastAPI templates) for dynamic content injection.

## 4. Acceptance Criteria
- [ ] Risk Notes with up to 12 policy terms/details fit on a single A4 page.
- [ ] The generated PDF has professional margins (e.g., 10-15mm) and a clear, readable structure.
- [ ] Coverage Details and Policy Terms are displayed in at least 2 columns where appropriate.
- [ ] The PDF generation process is integrated into the existing Policy/Risk Note workflow.

## 5. Out of Scope
- Support for multi-page Risk Notes (the primary goal is a one-page summary).
- User-editable Word templates (this track focuses on HTML-to-PDF).