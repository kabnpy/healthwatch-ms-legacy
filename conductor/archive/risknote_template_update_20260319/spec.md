# Specification: Update Risk Note Template

## Overview
This track involves updating the existing `risknote.html` Jinja2 template to match the visual structure and layout of the provided `motor_private-risknote-template.html` mockup. The goal is to move from a modern, minimalist layout to a more traditional, high-density grid-based design for Risk Notes, specifically tailored for Motor Private insurance while remaining adaptable to other classes.

## Functional Requirements
1.  **Layout Update:**
    -   Replace the current `section-table` with the compact, bordered table structure from the mockup.
    -   Use the `th[scope="row"]` pattern for labels on the left, with consistent border and padding.
    -   Implement the "space-between" layout for the **Insured** and **Class** rows to show secondary details (PIN, Policy Number) on the right.
2.  **Specific Row Implementations:**
    -   **Insured:** Display Name and PIN on the first line, followed by Address and Town.
    -   **Class:** Display Product Name and Policy Number on the same line.
    -   **Period:** Use the `&mdash;` separator for the start and end dates.
    -   **Cover:** Display the coverage description.
    -   **Vehicle Details:** Implement as a 4-column row (Reg No, Make, Year, Value) mapping from dynamic data.
    -   **Benefits & Limits / Excess / Special Clauses:** Use nested `inner-table` structures for these sections.
    -   **Premium:** Use the `premium` and `premium-total` classes to match the mockup's financial breakdown style.
3.  **Styling & Aesthetics (Hybrid):**
    -   Maintain the existing `base.html` letterhead and footer for cross-document consistency.
    -   In `risknote.html`, use the "Georgia" serif font for the content block (if possible without breaking PDF generation) or a similar high-quality serif.
    -   Apply the `1.5px solid #000` main table border and `1px solid #000` cell borders as shown in the mockup.
4.  **Data Mapping:**
    -   Map existing backend variables (`client`, `policy`, `risk_note`) to the dynamic input fields (Insured info, Vehicle Details, Period, Premium breakdown amounts).
    -   **Hardcoded Content (Motor Private Variant):** 
        -   The following sections will be hardcoded exactly as they appear in the mockup: "Benefits & Limits", "Excess", "Drivers", and "Special Clauses".
        -   The "Class" name ("Motor Private") and the "Cover" description ("Comprehensive Cover - ...") will be hardcoded.
    -   **Styling:** Use the exact styling and table structure from the mockup for the content area, while maintaining the modern header and footer from `base.html`.


## Non-Functional Requirements
-   **PDF Fidelity:** The template must render correctly via WeasyPrint, ensuring page breaks don't occur inside rows (using `page-break-inside: avoid`).
-   **Consistency:** The design must look professional and high-trust, aligning with the "Modern and Minimal" philosophy while adopting the requested traditional structure.

## Acceptance Criteria
-   [ ] The generated Risk Note PDF matches the table structure of `motor_private-risknote-template.html`.
-   [ ] The font is updated to a professional serif style within the document body.
-   [ ] Labels are uppercase and bolded on the left as per the mockup.
-   [ ] The financial breakdown includes a clear "Total" row with a thicker top border.
-   [ ] The letterhead and footer from `base.html` remain unchanged.

## Out of Scope
-   Modifying `base.html` layout or logic.
-   Changes to the backend `document_service.py` logic (unless absolutely necessary for data mapping).
-   Updates to other document templates (e.g., invoices, renewal notices).
