# Document Management Standardization Strategy

## 1. Objective
Create a consistent, reusable system for managing documents (correspondences, KYC, policy files) across any entity in the system.

## 2. Core Components

### `DocumentManager.tsx`
A unified component that combines the listing (`DataTable`) and the uploading (`AddDocument`) functionality.
- **Props:**
    - `ownerId: string`: The ID of the parent (Client, Policy).
    - `ownerType: 'client' | 'policy'`: To determine API endpoints and tagging.
    - `title: string`: Display header (e.g., "KYC Documents" vs "Policy Files").

### `DocumentColumns.tsx`
Standardized column definitions for all document tables.
- **Icon-based type detection:** Use different icons for PDF, Image, Word based on file extension.
- **Action Menu:** Open, Download, Delete, Edit Notes.

## 3. Implementation Plan

### Phase 1: Generalize the Component
- [x] Create `frontend/src/components/Common/DocumentManager.tsx` by refactoring `ClientDocuments.tsx`.
- [x] Implement `DocumentColumns.tsx` with the standardized "Action Menu".

### Phase 2: Client View Migration
- [x] Replace `ClientDocuments.tsx` with the new generic `DocumentManager`.
- [x] Add a `category` filter (available via DataTable search).

### Phase 3: Policy View Deployment
- [x] Update the `Documents` tab in `frontend/src/routes/_layout/policies.$policyId.tsx`.
- [x] Deploy `DocumentManager` with `ownerType="policy"`.

## 5. Progress Tracking
- **[2026-01-28]:** Strategy created and fully implemented. Unified document management across Client and Policy views.
