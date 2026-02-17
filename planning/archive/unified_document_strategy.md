# Strategy: Unified Document Upload & Management

## Objective
Consolidate all file handling into a single, robust workflow that replaces legacy "Correspondence" links with actual file storage and a unified UI.

---

## Step 1: Create a Reusable `FileUpload` Component
- **Task**: Extract the file input logic from `AddReceiptForm` into a standalone component.
- **Features**: Drag-and-drop support, file type validation (PDF/Images), and preview thumbnails.
- **Verifiable Outcome**: A single source of truth for all file selection UI.

## Step 2: Implement `UnifiedDocumentManager`
- **Task**: Create `frontend/src/components/Common/UnifiedDocumentManager.tsx`.
- **Logic**:
    - Uses `useDocuments(entityId, entityType)` to list files.
    - Uses `useUploadDocument()` for new files.
    - Uses `useDeleteDocument()` for removals.
- **UI**: A clean table or grid of documents with "View" buttons that trigger the `DocumentViewer` modal.

## Step 3: Define "Document Presets"
- **Task**: Create a configuration object that maps `entity_type` to common `document_types`.
- **Example**:
    - `Policy`: ["Logbook", "Valuation Report", "Police Abstract", "Policy Schedule"]
    - `Client`: ["KRA PIN Certificate", "National ID / Passport", "Certificate of Incorporation"]
    - `Claim`: ["Accident Photos", "Repair Estimate", "Claim Form"]
- **Verifiable Outcome**: The upload form has a context-aware dropdown, reducing typing errors.

## Step 4: Integrate the "Lightbox" Viewer
- **Task**: Update the document list actions.
- **Action**: Instead of `window.open(url)`, the "View" button should set the `selectedDoc` state in the parent view, opening the `DocumentViewer` (lightbox) we just improved.
- **Verifiable Outcome**: Seamless "In-App" document viewing experience.

## Step 5: Migration & Cleanup
- **Task**: Replace all instances of the old `DocumentManager` (the correspondence-based one) with the new `UnifiedDocumentManager`.
- **Target Locations**:
    - `PolicyDashboard`
    - `ClientOverview`
    - `ClaimDetail` (future)
- **Verifiable Outcome**: "Correspondence" is reserved for communication logs (emails/notes), and "Documents" handles all physical files.

---

## Why this approach?
1. **Consistency**: One way to upload, one way to view, one way to delete.
2. **Data Integrity**: Files are linked to the correct entities via UUIDs and Enums.
3. **Future Proofing**: Easily swap Local Storage for S3/Blob storage at the provider level.
