from aiogram import Router
from presentation.handlers import start as start_handlers
from presentation.handlers import admin as admin_handlers

def build_root_router() -> Router:
    router = Router()
    router.include_router(admin_handlers.router)
    router.include_router(start_handlers.router)

    return router
