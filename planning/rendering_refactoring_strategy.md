# Strategy: Decoupling Rendering Logic from Database

## Goal
Remove presentation-specific metadata (`display_type`) from the database and implement a frontend-driven layout engine. Fix the issue where new seed data is not appearing in the UI.

## 1. Architectural Change
We will move the responsibility of choosing the UI component from the JSON schema to a Frontend **Layout Registry**.

### Current (Counter-pattern)
DB: `{"key": "reg_no", "section": "VEHICLE DETAILS", "display_type": "grid-row"}`

### New (Semantic/Inferred)
DB: `{"key": "reg_no", "section": "VEHICLE DETAILS"}`
Frontend: `getComponent(section="VEHICLE DETAILS", fields=[...])` -> returns `<RiskNoteGridRow />`

## 2. Implementation Steps

### Phase 1: Frontend Layout Registry
- [x] Create `frontend/src/utils/layoutRegistry.ts`:
    - [x] Define logic to map `section` names to layouts (e.g., "EXCESS" -> List, "VEHICLE DETAILS" -> Grid).
    - [x] Add logic to handle "Included/Yes" values for clauses automatically.
- [x] Update `RiskNoteTemplate.tsx`:
    - [x] Remove reliance on `field.display_type`.
    - [x] Use the registry to determine rendering style.

### Phase 2: Backend Cleanup & Robust Seeding
- [x] Update `backend/app/seed_mock_data.py`:
    - [x] Remove `display_type` from all product definitions.
    - [x] **Fix Visibility**: Change seeding logic to *update* existing products if they differ, rather than just skipping if they exist.
- [x] Run `python backend/app/seed_mock_data.py` to refresh the database.

### Phase 3: Verification
- [x] Verify that Motor Private displays "VEHICLE DETAILS" as a grid.
- [x] Verify that Personal Accident displays "BENEFITS" as a list.
- [x] Ensure no `display_type` exists in the backend models/JSON.

## 3. Git Commit Strategy
1. "refactor(frontend): create layout registry for risk notes"
2. "feat(backend): update seeding logic to sync existing products"
3. "cleanup(db): remove presentation metadata from seed data"
