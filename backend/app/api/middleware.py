import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.middleware")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        # Process the request
        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        # Log metadata
        log_dict = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration": f"{process_time:.4f}s",
        }

        logger.info(f"Request: {log_dict}")

        return response
