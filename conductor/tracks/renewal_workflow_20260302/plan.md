# Implementation Plan: Renewal Workflow Management

## Phase 0: Project Setup & Branching [checkpoint: bd0e43d]
*   **Goal:** Initialize the development environment for the new feature.
- [x] Task: Create a new git branch for the renewal workflow.
    - [x] Branch name: `feat/renewal-workflow`.

*   - [x] Task: Ensure the current workspace is synchronized and passing all existing tests.
*   - [x] Task: Conductor - User Manual Verification 'Project Setup' (Protocol in workflow.md)

## Phase 1: Data Model & Core Logic (Backend) [checkpoint: 85ff5ed]
*   **Goal:** Enhance the data model to support renewal statuses and implement logic to identify expiring policies.
*   - [x] Task: Update `PolicyStatus` and `RiskNoteStatus` enums. [6f665a8] [fe22d38]
    *   - [x] Add `RENEWAL_INVITED` and `RENEWAL_CONFIRMED` to the status definitions.
    *   - [x] Add `LAPSED` status for expired covers.
*   - [x] Task: Implement "Expiring Soon" query logic in the service layer. [fe22d38]
    *   - [x] Create a service method to retrieve policies expiring in exactly 30 days and 7 days.
    *   - [x] Ensure the query accounts for the latest `RiskNote` per `Policy`.
*   - [x] Task: Write unit tests for date-based filtering. [fe22d38]
    *   - [x] Verify that policies are correctly identified for the 30-day and 7-day windows.
*   - [x] Task: Conductor - User Manual Verification 'Data Model & Core Logic' (Protocol in workflow.md)

## Phase 2: Email Automation & Job Scheduling [checkpoint: 922f9c7]
*   **Goal:** Implement the automated email notification system and the scheduling mechanism.
*   - [x] Task: Design and implement Renewal Email templates. [a07e57c]
    *   - [x] Create HTML templates for the 30-day "Renewal Invitation" and 7-day "Reminder".
    *   - [x] Include dynamic placeholders for policy number, client name, and premium.
*   - [x] Task: Implement the Email Dispatcher service. [accd106]
    *   - [x] Create logic to send emails via the configured SMTP/Mail service.
    *   - [x] Add error handling and logging for failed dispatches.
*   - [x] Task: Setup the automated "Renewal Watcher" job. [650013e]
    *   - [x] Implement a daily background task (e.g., via Celery or a script) that runs the expiry check and triggers emails.
    *   - [x] Write tests to ensure the job doesn't send duplicate emails for the same policy/period.
*   - [x] Task: Conductor - User Manual Verification 'Email Automation' (Protocol in workflow.md)

## Phase 3: Frontend Dashboard & Workflow UI
*   **Goal:** Surface the renewal workflow to agency staff via the dashboard.
*   - [x] Task: Implement the "Renewals Due" dashboard view. [d648b42] [af29a1c]
    *   - [x] Add a new filter or tab to the Insurance Dashboard displaying policies expiring within 30 days.
    *   - [x] Include status badges for `Renewal Invited` and `Renewal Confirmed`.
*   - [x] Task: Create the "Record Renewal Invitation" form. [af29a1c] [d8a3d61]
    *   - [x] Build a UI component to manually input updated terms from an insurer notice.
    *   - [x] Implement file upload support for the insurer's PDF notice.
*   - [ ] Task: Connect frontend actions to backend status transitions.
    *   - [ ] Add buttons to manually trigger a renewal invite email or confirm a renewal.
*   - [ ] Task: Conductor - User Manual Verification 'Frontend Integration' (Protocol in workflow.md)
