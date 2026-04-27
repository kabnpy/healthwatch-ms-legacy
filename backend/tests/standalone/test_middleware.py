import sys
from unittest.mock import MagicMock, patch

# Aggressive mocking to prevent database connection on import
mock_engine = MagicMock()
mock_session = MagicMock()
sys.modules["app.core.db"] = MagicMock(engine=mock_engine, Session=mock_session)

import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_logging_middleware_captures_request(client: TestClient):
    """Verify that LoggingMiddleware logs request details."""
    with patch("app.api.middleware.logger.info") as mock_logger:
        # health-check usually doesn't hit DB
        response = client.get("/api/v1/utils/health-check")
        
        assert mock_logger.called
        log_message = mock_logger.call_args[0][0]
        assert "Request:" in log_message
        assert "'method': 'GET'" in log_message
        # FastAPI might add or normalize trailing slashes
        assert "/api/v1/utils/health-check" in log_message
