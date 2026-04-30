from app.models import Policy, PolicyPublic, RiskNote, RiskNotePublic
from app.services.risknote import risknote_service


def prepare_risknote_public(risk_note: RiskNote) -> RiskNotePublic:
    """
    Populate RiskNotePublic with computed data using RiskNoteService.
    """
    res = RiskNotePublic.model_validate(risk_note)
    res.special_clauses = risknote_service.get_special_clauses(risk_note)
    res.invoice_number = risknote_service.get_invoice_number(risk_note)
    return res


def prepare_policy_public(policy: Policy) -> PolicyPublic:
    """
    Populate PolicyPublic with computed data from latest Risk Note.
    """
    from app.models import RiskNoteStatus

    res = PolicyPublic.model_validate(policy)

    # Find the latest ISSUED risk note
    # Relationship is ordered by effective_date desc, created_at desc
    active_rn = next(
        (rn for rn in policy.risk_notes if rn.status == RiskNoteStatus.ISSUED), None
    )

    # If no ISSUED note, take the first one (most recent)
    if not active_rn and policy.risk_notes:
        active_rn = policy.risk_notes[0]

    if active_rn:
        res.active_note = prepare_risknote_public(active_rn)

    if policy.client:
        from app.models import ClientPublic

        res.client = ClientPublic.model_validate(policy.client)

    return res
