from datetime import date, timedelta
from typing import Any
import uuid
from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload
from app.models import Policy, RiskNote, RiskNoteStatus, PolicyStatus
from app.utils import send_email, render_email_template
from app.core.config import settings

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
        target_date = date.today() + timedelta(days=days)
        
        latest_rn_sub = (
            select(RiskNote.policy_id, func.max(RiskNote.coverage_end).label("max_end"))
            .where(RiskNote.status == RiskNoteStatus.ISSUED)
            .group_by(RiskNote.policy_id)
            .subquery()
        )
        
        statement = (
            select(Policy)
            .join(latest_rn_sub, Policy.id == latest_rn_sub.c.policy_id)
            .where(latest_rn_sub.c.max_end <= target_date)
            .where(latest_rn_sub.c.max_end >= date.today())
            .options(selectinload(Policy.risk_notes), selectinload(Policy.client))
        )
        return list(session.exec(statement).all())

    @staticmethod
    def send_renewal_invitation(session: Session, *, policy: Policy) -> None:
        """
        Sends a renewal invitation email to the client.
        """
        if not policy.client or not policy.client.email:
            return

        latest_rn = next((rn for rn in policy.risk_notes if rn.status == RiskNoteStatus.ISSUED), None)
        if not latest_rn:
            return

        project_name = settings.PROJECT_NAME
        subject = f"{project_name} - Renewal Invitation for {policy.policy_number}"
        link = f"{settings.FRONTEND_HOST}/policies/{policy.id}"
        
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
        link = f"{settings.FRONTEND_HOST}/policies/{policy.id}"
        
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

    @staticmethod
    def run_daily_renewal_checks(session: Session) -> None:
        """
        Runs the daily automated renewal tasks.
        """
        # 1. 30-day invitations
        to_invite = renewal_service.get_policies_expiring_exactly_in(session, days=30)
        for policy in to_invite:
            renewal_service.send_renewal_invitation(session, policy=policy)
            policy.status = PolicyStatus.RENEWAL_INVITED
            session.add(policy)
        
        # 2. 7-day reminders
        to_remind = renewal_service.get_policies_expiring_exactly_in(session, days=7)
        for policy in to_remind:
            # Only remind if not yet renewed/confirmed
            if policy.status in [PolicyStatus.ACTIVE, PolicyStatus.RENEWAL_INVITED]:
                renewal_service.send_renewal_reminder(session, policy=policy)
        
        session.commit()

renewal_service = RenewalService()
