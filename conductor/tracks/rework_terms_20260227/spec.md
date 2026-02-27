# Specification: Rework Cover Snapshot Terms

## 1. Overview
The current implementation of `cover_snapshot` within `RiskNote` uses complex structuring for policy terms (benefits, excesses, special clauses). This rework aims to simplify this by storing terms as plain text strings within a generic `terms` object. This will improve data maintainability and simplify the logic for rendering these terms on the dashboard and other view pages.

## 2. Functional Requirements
- **Backend:**
    - Update the `RiskNote` and related schemas to use a `terms` dictionary in the `cover_snapshot`.
    - Each entry in the `terms` dictionary should be a plain text string.
    - Implement a migration to convert existing structured terms to plain text for all active policies.
    - Ensure new policy transactions (New Business, Renewal, Endorsement) populate these text fields.
- **Frontend:**
    - Update the Catalog and Policy Detail view pages to fetch and display the new `terms` structure.
    - Render terms as simple text blocks (preserving newlines).
    - Ensure the UI handles various products (Motor, Fire, etc.) by iterating over the keys in the `terms` object.

## 3. Non-Functional Requirements
- **Data Integrity:** The migration must accurately preserve existing term data.
- **Performance:** Ensure that fetching and rendering these text blocks is efficient.
- **Type Safety:** Maintain strict TypeScript types for the updated `cover_snapshot`.

## 4. Acceptance Criteria
- [ ] Existing policies have their terms correctly migrated to plain text strings.
- [ ] New policy issuances store terms in the new flat `terms` structure.
- [ ] The dashboard and policy view pages correctly display these terms for different products.
- [ ] Terms are rendered clearly with preserved newlines.

## 5. Out of Scope
- Rich text editing (Markdown) for terms in this track.
- Changes to the insurer's product definition beyond the `cover_snapshot` structure.
