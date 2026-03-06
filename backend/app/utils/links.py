import uuid
from app.core.config import settings

def get_policy_view_url(policy_id: uuid.UUID, client_id: uuid.UUID) -> str:
    """Returns the frontend URL for a specific policy dashboard."""
    return f"{settings.FRONTEND_HOST}/clients/{client_id}/policies/{policy_id}"
