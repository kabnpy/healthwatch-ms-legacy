from datetime import date, timedelta
from typing import Any
import uuid
from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload
from app.models import Policy, RiskNote, RiskNoteStatus

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
            .options(selectinload(Policy.risk_notes))
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
            .options(selectinload(Policy.risk_notes))
        )
        return list(session.exec(statement).all())

renewal_service = RenewalService()
