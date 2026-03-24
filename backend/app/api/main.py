"""
Purpose: Register all API route modules into the main API router

Structure:
    api_router (APIRouter): output - Combined router with all route modules

Relationships:
    Consumes: api.routes.login, api.routes.users, api.routes.utils, api.routes.items, api.routes.private
    Produces: api_router (consumed by app.main)

Note:
    Private routes only registered when ENVIRONMENT=local.
"""

from fastapi import APIRouter

from app.api.routes import items, login, private, users, utils
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
