# Strategy: Risk Note Template Refinement

## Goal
Transition the Risk Note rendering from a strict table-row layout to a flexible layout that supports list-based details for specific sections (e.g., "Benefits and Limits").

## 1. Optimal Data Shape for Product Details
Currently, `product_details` is a flat list of field definitions:
```json
[
  {
    "key": "sum_insured",
    "label": "Sum Insured",
    "field_type": "input",
    "section": "Cover Details"
  }
]
```

### Proposed Enhancement
We will use a `display_type` property in the `product_details` JSON to control rendering logic.

**`display_type` options:**
- `table-row` (Default): Label on left, Value on right.
- `list-item`: Full width, bulleted or simple list style.

## 2. Implementation Steps

### Phase 1: Preparation
- [ ] Create git branch `feat/risk-note-layout-refinement`
- [ ] Audit current `product_details` usage in the database/seed data

### Phase 2: Frontend UI Components
- [ ] Create `RiskNoteListItem.tsx` for list-style rendering.
- [ ] Update `RiskNoteTemplate.tsx`:
    - Refine aggregation logic to respect `display_type`.
    - Implement conditional rendering between `RiskNoteRow` and `RiskNoteListItem`.

### Phase 3: Data Migration/Seeding
- [ ] Update `backend/app/seed_mock_data.py` to include `display_type: "list-item"` for benefits.

### Phase 4: Verification
- [ ] Verify rendering of "Benefits and Limits" as a list.
- [ ] Ensure "Core Details" still use the table-row layout.

## 3. Git Commit Strategy
- Small, targeted commits:
  1. "docs: add risk note refinement strategy"
  2. "feat(frontend): add RiskNoteListItem component"
  3. "feat(frontend): update RiskNoteTemplate to support list rendering"
  4. "feat(backend): update product seed data with display_type"
