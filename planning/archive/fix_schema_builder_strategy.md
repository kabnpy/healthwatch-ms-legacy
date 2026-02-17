# Strategy: Fix Schema Builder View

## Problem
The "Form Schema" tab in the Product Detail view is either not rendering or appearing broken.

## Potential Root Causes
1. **Component Crash**: A missing or incorrectly imported UI component might be causing a runtime error.
2. **Data Initialization**: `useFieldArray` might not be correctly picking up the `product_details` from the form's `defaultValues`.
3. **Form Context Conflict**: `ProductDetailContent` uses a parent `FormProvider`, while `ProductForm` (nested inside) creates its own `useForm` instance. This duplication can lead to state desynchronization.
4. **Visibility/Layout**: The component might be rendering but hidden due to CSS or lack of content.

## Plan of Action

### Phase 1: Diagnostics & Component Cleanup
- [ ] **Task 1.1**: Verify `SchemaBuilder` doesn't crash on mount by adding basic logging.
- [ ] **Task 1.2**: Ensure `ProductDetailContent` is passing the correct methods to `FormProvider`.
- [ ] **Task 1.3**: Confirm `product_details` is an array before passing to `useFieldArray`.

### Phase 2: Form Architecture Refactoring
- [ ] **Task 2.1**: Update `ProductForm` to be "Context Aware". If it's inside a `FormProvider`, it should use the existing context instead of creating a new `useForm`.
- [ ] **Task 2.2**: Standardize how `ProductDetailContent` handles the "Save" action for both General and Schema tabs.

### Phase 3: UI/UX & Layout Fixes
- [ ] **Task 3.1**: Add a fallback view in `SchemaBuilder` if fields are empty but initialized.
- [ ] **Task 3.2**: Add explicit background and padding to the Schema tab content.

### Phase 4: Verification
- [ ] **Task 4.1**: Run `npm run build` to catch any remaining type issues.
- [ ] **Task 4.2**: Manually verify adding/removing fields in the UI.

---

## Git Strategy
- **Branch**: `fix/schema-builder-rendering`
- **Commits**:
  - `fix(frontend): resolve form context conflict in product detail view`
  - `feat(frontend): add debug logging and fallback to schema builder`
  - `style(frontend): improve schema builder layout and visibility`
