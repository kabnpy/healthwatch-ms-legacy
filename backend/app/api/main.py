from fastapi import APIRouter

from app.api.routes import (
    claims,
    clients,
    insurers,
    items,
    login,
    payments,
    policies,
    private,
    products,
    users,
    utils,
)
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(insurers.router, prefix="/insurers", tags=["insurers"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(policies.router, prefix="/policies", tags=["policies"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(claims.router, prefix="/claims", tags=["claims"])


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
