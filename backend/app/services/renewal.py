import logging
from datetime import date, datetime, timedelta

from sqlalchemy.orm import selectinload
from sqlmodel import Session, func, select

from app.core.config import settings
from app.models import (
    Correspondence,
    CorrespondenceCreate,
    Policy,
    PolicyStatus,
    RiskNote,
    RiskNoteStatus,
)
from app.utils import render_email_template, send_email


class RenewalService:
    @staticmethod
    def get_policies_expiring_exactly_in(session: Session, days: int) -> list[Policy]:
        """
        Retrieves policies whose latest issued Risk Note expires exactly 'days' from today.
        """
        target_date = date.today() + timedelta(days=days)

        # Subquery to get the latest coverage_end for each policy's issued risk notes
        latest_rn_sub = (
            select(RiskNote.policy_id, func.max(RiskNote.coverage_end).label("max_end"))
            .where(RiskNote.status == RiskNoteStatus.ISSUED)
            .where(RiskNote.deleted_at == None)
            .group_by(RiskNote.policy_id)
            .subquery()
        )

        statement = (
            select(Policy)
            .join(latest_rn_sub, Policy.id == latest_rn_sub.c.policy_id)
            .where(latest_rn_sub.c.max_end == target_date)
            .options(selectinload(Policy.risk_notes), selectinload(Policy.client))
        )
        return list(session.exec(statement).all())

    @staticmethod
    def get_policies_expiring_within(session: Session, days: int) -> list[Policy]:
        """
        Retrieves policies whose latest issued Risk Note expires within 'days' from today.
        """
        from app.crud import get_policies
        return get_policies(session, expiring_within=days)

    @staticmethod
    def send_renewal_invitation(session: Session, *, policy: Policy) -> None:
        """
        Sends a renewal invitation email to the client.
        """
        if not policy.client or not policy.client.email:
            return

        # Only proceed if a manually prepped invitation note exists
        latest_rn = next(
            (rn for rn in policy.risk_notes if rn.status == RiskNoteStatus.RENEWAL_INVITED),
            None
        )
        if not latest_rn:
            logging.info(f"Skipping auto-invite for {policy.policy_number}: No 'Renewal Invited' draft found.")
            return

        project_name = settings.PROJECT_NAME
        subject = f"{project_name} - Renewal Invitation for {policy.policy_number}"
        # Point to the specific policy view in the frontend
        link = f"{settings.FRONTEND_HOST}/clients/{policy.client_id}/policies/{policy.id}"

        html_content = render_email_template(
            template_name="renewal_invitation.html",
            context={
                "project_name": project_name,
                "client_name": policy.client.name,
                "policy_number": policy.policy_number,
                "expiry_date": latest_rn.coverage_end.strftime("%d %b %Y"),
                "premium": f"{latest_rn.total_amount:,.2f}",
                "link": link,
            },
        )

        send_email(
            email_to=policy.client.email,
            subject=subject,
            html_content=html_content,
        )

        # Update policy status to reflect invitation
        policy.status = PolicyStatus.RENEWAL_INVITED
        session.add(policy)

        # Log notification in client correspondence history
        db_correspondence = Correspondence.model_validate(
            CorrespondenceCreate(
                client_id=policy.client_id,
                subject=subject,
                summary=f"Renewal invitation dispatched for policy {policy.policy_number}. Coverage Expiry: {latest_rn.coverage_end}.",
                file_path="SYSTEM_GENERATED_EMAIL",
                date_logged=datetime.now()
            )
        )
        session.add(db_correspondence)

    @staticmethod
    def send_renewal_reminder(session: Session, *, policy: Policy) -> None:
        """
        Sends a 7-day renewal reminder email to the client.
        """
        if not policy.client or not policy.client.email:
            return

        latest_rn = next((rn for rn in policy.risk_notes if rn.status == RiskNoteStatus.ISSUED), None)
        if not latest_rn:
            return

        project_name = settings.PROJECT_NAME
        subject = f"{project_name} - Renewal Reminder: {policy.policy_number}"
        # Point to the specific policy view in the frontend
        link = f"{settings.FRONTEND_HOST}/clients/{policy.client_id}/policies/{policy.id}"

        html_content = render_email_template(
            template_name="renewal_reminder.html",
            context={
                "project_name": project_name,
                "client_name": policy.client.name,
                "policy_number": policy.policy_number,
                "expiry_date": latest_rn.coverage_end.strftime("%d %b %Y"),
                "link": link,
            },
        )

        send_email(
            email_to=policy.client.email,
            subject=subject,
            html_content=html_content,
        )

        # Log notification in client correspondence history
        db_correspondence = Correspondence.model_validate(
            CorrespondenceCreate(
                client_id=policy.client_id,
                subject=subject,
                summary=f"7-day renewal reminder dispatched for policy {policy.policy_number}. Coverage Expiry: {latest_rn.coverage_end}.",
                file_path="SYSTEM_GENERATED_EMAIL",
                date_logged=datetime.now()
            )
        )
        session.add(db_correspondence)

    @staticmethod
    def run_daily_renewal_checks(session: Session) -> None:
        """
        Runs the daily automated renewal tasks.
        """
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # 1. 30-day invitations
        to_invite = renewal_service.get_policies_expiring_exactly_in(session, days=30)
        if to_invite:
            # Collect subjects to check for idempotency in bulk
            invitation_subjects = {
                f"{settings.PROJECT_NAME} - Renewal Invitation for {p.policy_number}"
                for p in to_invite
            }

            existing_invitations_statement = (
                select(Correspondence.subject)
                .where(Correspondence.subject.in_(list(invitation_subjects)))
                .where(Correspondence.date_logged >= today_start)
            )
            sent_invitation_subjects = set(session.exec(existing_invitations_statement).all())

            for policy in to_invite:
                subject = f"{settings.PROJECT_NAME} - Renewal Invitation for {policy.policy_number}"
                if subject not in sent_invitation_subjects and policy.status != PolicyStatus.RENEWAL_INVITED:
                    try:
                        renewal_service.send_renewal_invitation(session, policy=policy)
                        # Commit per-item to ensure recovery even on partial failure
                        session.commit()
                    except Exception as e:
                        logging.error(f"Failed to send invitation for {policy.policy_number}: {e}")
                        session.rollback()

        # 2. 7-day reminders
        to_remind = renewal_service.get_policies_expiring_exactly_in(session, days=7)
        if to_remind:
            # Collect subjects to check for idempotency in bulk
            reminder_subjects = {
                f"{settings.PROJECT_NAME} - Renewal Reminder: {p.policy_number}"
                for p in to_remind
            }

            existing_reminders_statement = (
                select(Correspondence.subject)
                .where(Correspondence.subject.in_(list(reminder_subjects)))
                .where(Correspondence.date_logged >= today_start)
            )
            sent_reminder_subjects = set(session.exec(existing_reminders_statement).all())

            for policy in to_remind:
                subject = f"{settings.PROJECT_NAME} - Renewal Reminder: {policy.policy_number}"
                if subject not in sent_reminder_subjects and policy.status in [PolicyStatus.ACTIVE, PolicyStatus.RENEWAL_INVITED]:
                    try:
                        renewal_service.send_renewal_reminder(session, policy=policy)
                        # Commit per-item to ensure recovery even on partial failure
                        session.commit()
                    except Exception as e:
                        logging.error(f"Failed to send reminder for {policy.policy_number}: {e}")
                        session.rollback()

renewal_service = RenewalService()
