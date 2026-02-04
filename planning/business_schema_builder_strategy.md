# Strategy: Business-First Schema Builder

## Objective
Transform the technical "Schema Builder" into an intuitive, non-technical interface for insurance admins.

## Core UX Principles
1. **No "Database Keys"**: Automatically generate keys from labels (e.g., "Reg No" -> `reg_no`). Hide the raw key in an "Advanced" toggle.
2. **Visual Grouping**: Group fields into "Sections" (e.g., VEHICLE DETAILS) so users don't type the section name for every field.
3. **Simplified Types**: Replace "Logic Type + Input Style" with intuitive definitions:
   - "User Input (Text/Number/Date)"
   - "Fixed Policy Benefit" (Static)
   - "Optional Add-on" (Optional)
4. **Immediate Feedback**: Use a layout that looks closer to the final Risk Note.

## Measurable Tasks

### Phase 1: Data Abstraction
- [ ] **Task 1.1**: Implement a `slugify` utility to auto-generate unique keys from labels.
- [ ] **Task 1.2**: Create a mapping between "Friendly Types" and the technical `field_type/input_type` properties.

### Phase 2: Section-Based UI
- [ ] **Task 2.1**: Refactor `SchemaBuilder` to group the `product_details` array by the `section` property for display.
- [ ] **Task 2.2**: Implement "Add Section" and "Add Field to Section" actions.
- [ ] **Task 2.3**: Allow renaming sections which updates all child fields.

### Phase 3: Technical Hiding
- [ ] **Task 3.1**: Hide the "Database Key" and "Section" inputs behind an "Advanced Settings" toggle.
- [ ] **Task 3.2**: Automatically sync the Key when the Label changes (unless manually overridden).

### Phase 4: Polish
- [ ] **Task 4.1**: Add icons for different field types (e.g., Calendar for Date, Hash for Number).
- [ ] **Task 4.2**: Standardize the "Static Value" input to show up only when "Fixed Benefit" is selected.

---

## Git Strategy
- **Branch**: `refactor/business-friendly-builder`
- **Commit**: `feat(frontend): implement section-based schema builder with auto-key generation`
