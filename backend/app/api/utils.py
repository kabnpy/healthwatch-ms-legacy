from app.models import Policy, PolicyPublic

def prepare_policy_public(policy: Policy) -> PolicyPublic:
    """
    Populate PolicyPublic with computed data from latest Risk Note.
    """
    # PolicyPublic properties are now computed properties that check for self.risk_notes
    return PolicyPublic.model_validate(policy)
