# Strategy: Remove Primary Contact Column

## Goal
Remove the "Primary Contact" column from the Clients table view in the frontend.

## 1. Analysis
- **Current State**: The `frontend/src/components/Clients/columns.tsx` file defines the columns for the Clients table. It currently includes a "Primary Contact" column which displays the name of the first contact from the `contacts` array.
- **Desired State**: The "Primary Contact" column should be removed. The underlying data (`contacts` field) will remain in the API response and model as it might be used elsewhere (e.g., Client Overview), but it will not be displayed in the main table list.

## 2. Plan
- **Step 1**: Edit `frontend/src/components/Clients/columns.tsx`.
- **Step 2**: Remove the column definition object with `header: "Primary Contact"`.
- **Step 3**: Verify the change by checking if the column is gone (visually or via code review).

## 3. Atomic Steps
- [x] **Step 3.1**: Remove the column definition from `frontend/src/components/Clients/columns.tsx`.
- [x] **Step 3.2**: Unify the styling for the "Client Type" badge in `frontend/src/components/Clients/columns.tsx`.
