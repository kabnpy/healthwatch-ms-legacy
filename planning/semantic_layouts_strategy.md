# Strategy: Semantic & Flexible Document Layouts

## Objective
Enable diverse data presentation styles (Key-Value, Lists, Descriptive Blocks) and transition the Risk Note to a semantic table-based layout for professional printing and reduced cognitive load.

## 1. Defining Section Types
We will support three primary layout modes for every section in a product:

| Type | Structure | Use Case |
| :--- | :--- | :--- |
| **TABLE** | 2 Columns: Label | Value | Benefits, Excesses, Vehicle Details |
| **LIST** | 1 Column: Bulleted/Numbered List | Special Clauses, Exclusions |
| **BLOCK** | 1 Column: Full-width text block | Occupation, Narrative descriptions |

## 2. Technical Decisions
- **Explicit Config**: Layout types will be saved in `Product.section_configs` (JSON) to remove guesswork from the frontend.
- **Semantic HTML**: Use `<table>` instead of `CSS Grid` for the document core to improve print reliability and visual consistency.

## 3. Measurable Tasks

### Phase 1: Backend Foundation
- [ ] **Task 1.1**: Add `section_configs` field to `ProductBase` and `ProductUpdate` models.
- [ ] **Task 1.2**: Update mock data to utilize these new configurations.

### Phase 2: Advanced Editor UI
- [ ] **Task 2.1**: Add a "Section Layout" toggle to the `SchemaBuilder` headers.
- [ ] **Task 2.2**: Implement conditional rendering for rows (e.g., hide labels in "LIST" mode).
- [ ] **Task 2.3**: Auto-generate unique keys for list items to maintain data integrity.

### Phase 3: Risk Note Refactor
- [ ] **Task 3.1**: Rewrite `RiskNoteTemplate` using `<table>`.
- [ ] **Task 3.2**: Implement layout-specific rendering components (`TableSection`, `ListSection`, `BlockSection`).
- [ ] **Task 3.3**: Ensure borders and spacing match the established "Minimal Invoice" brand style.

---

## 4. Git Strategy
- **Branch**: `refactor/semantic-table-layouts`
- **Commits**:
  - `feat(backend): add explicit section configuration to product model`
  - `feat(frontend): implement section layout selector in product editor`
  - `refactor(frontend): transition risk note to semantic table-based layout`
