# Track Specification: Renewal Workflow Management

## Overview
This track defines the end-to-end workflow for managing policy renewals within the agency. The goal is to ensure that no policy expires without proper review, client notification, and follow-up. The system will track policies approaching expiry, facilitate the recording of insurer renewal terms, and manage the communication lifecycle with the client via email.

## Functional Requirements

### 1. Renewal Monitoring & Dashboard
- **Expiry Visibility:** A dedicated "Renewals Due" dashboard or filter that highlights all active policies expiring within the next 30 days.
- **Status Tracking:** Support for the following workflow-specific statuses:
    - `Renewal Invited`: The agency has received the notice from the insurer and sent an invitation to the client.
    - `Renewal Confirmed`: The client has agreed to the renewal terms and the agency is awaiting final processing/payment.
    - `Lapsed/Expired`: The policy has passed its expiry date without a renewal being finalized.

### 2. Renewal Invitation Handling
- **Manual Recording:** Staff can record the terms of a renewal notice received from an insurer (e.g., new premium, updated cover details).
- **Document Attachment:** Support for uploading the insurer's PDF renewal notice to the `Policy` or `Risk Note` record.

### 3. Automated Communication (Email)
- **Initial Invite:** The system will automatically generate and send a renewal notice email to the client 30 days before expiry.
- **7-Day Reminder:** A follow-up email reminder will be sent to the client if the renewal status is not "Confirmed" or "Renewed" 7 days before expiry.
- **Template Content:** Emails will include current policy details, proposed renewal terms (if recorded), and payment instructions.

### 4. Transition to New Cover
- **Renewal Issuance:** When a renewal is finalized, the system will create a new `Risk Note` snapshot linked to the same `Policy` entity, ensuring historical continuity.

## Non-Functional Requirements
- **Precision:** Date-based triggers must account for leap years and varying month lengths accurately.
- **Audit Trail:** All status changes and email dispatches must be logged in the policy's relationship history.

## Acceptance Criteria
- [ ] Staff can view a list of policies expiring within the current 30-day window.
- [ ] A user can manually record renewal terms from an insurer notice.
- [ ] Automated emails are successfully dispatched at the 30-day and 7-day marks.
- [ ] The policy status correctly transitions to `Renewal Invited` upon notification and `Lapsed` upon expiry if not renewed.
- [ ] The renewed policy maintains a link to the historical data of the previous cover.

## Out of Scope
- SMS and WhatsApp notifications.
- Automated parsing of insurer renewal notice emails.
- Multi-quote comparison tools (facilitating multiple competing renewal options).
