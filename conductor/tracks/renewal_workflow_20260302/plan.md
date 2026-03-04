# Implementation Plan: Renewal Workflow Management

## Phase 0: Project Setup & Branching [checkpoint: bd0e43d]
*   **Goal:** Initialize the development environment for the new feature.
- [x] Task: Create a new git branch for the renewal workflow.
    - [x] Branch name: `feat/renewal-workflow`.

*   - [x] Task: Ensure the current workspace is synchronized and passing all existing tests.
*   - [ ] Task: Conductor - User Manual Verification 'Project Setup' (Protocol in workflow.md)

## Phase 1: Data Model & Core Logic (Backend)
*   **Goal:** Enhance the data model to support renewal statuses and implement logic to identify expiring policies.
*   - [x] Task: Update `PolicyStatus` and `RiskNoteStatus` enums. [6f665a8]
    *   - [x] Add `RENEWAL_INVITED` and `RENEWAL_CONFIRMED` to the status definitions.
    *   - [x] Add `LAPSED` status for expired covers.
*   - [ ] Task: Implement "Expiring Soon" query logic in the service layer.
    *   - [ ] Create a service method to retrieve policies expiring in exactly 30 days and 7 days.
    *   - [ ] Ensure the query accounts for the latest `RiskNote` per `Policy`.
*   - [ ] Task: Write unit tests for date-based filtering.
    *   - [ ] Verify that policies are correctly identified for the 30-day and 7-day windows.
*   - [ ] Task: Conductor - User Manual Verification 'Data Model & Core Logic' (Protocol in workflow.md)

## Phase 2: Email Automation & Job Scheduling
*   **Goal:** Implement the automated email notification system and the scheduling mechanism.
*   - [ ] Task: Design and implement Renewal Email templates.
    *   - [ ] Create HTML templates for the 30-day "Renewal Invitation" and 7-day "Reminder".
    *   - [ ] Include dynamic placeholders for policy number, client name, and premium.
*   - [ ] Task: Implement the Email Dispatcher service.
    *   - [ ] Create logic to send emails via the configured SMTP/Mail service.
    *   - [ ] Add error handling and logging for failed dispatches.
*   - [ ] Task: Setup the automated "Renewal Watcher" job.
    *   - [ ] Implement a daily background task (e.g., via Celery or a script) that runs the expiry check and triggers emails.
    *   - [ ] Write tests to ensure the job doesn't send duplicate emails for the same policy/period.
*   - [ ] Task: Conductor - User Manual Verification 'Email Automation' (Protocol in workflow.md)

## Phase 3: Frontend Dashboard & Workflow UI
*   **Goal:** Surface the renewal workflow to agency staff via the dashboard.
*   - [ ] Task: Implement the "Renewals Due" dashboard view.
    *   - [ ] Add a new filter or tab to the Insurance Dashboard displaying policies expiring within 30 days.
    *   - [ ] Include status badges for `Renewal Invited` and `Renewal Confirmed`.
*   - [ ] Task: Create the "Record Renewal Invitation" form.
    *   - [ ] Build a UI component to manually input updated terms from an insurer notice.
    *   - [ ] Implement file upload support for the insurer's PDF notice.
*   - [ ] Task: Connect frontend actions to backend status transitions.
    *   - [ ] Add buttons to manually trigger a renewal invite email or confirm a renewal.
*   - [ ] Task: Conductor - User Manual Verification 'Frontend Integration' (Protocol in workflow.md)
