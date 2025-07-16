from aiogram import Router
from bot.handlers.auth import router as auth_router
from bot.handlers.commands import router as commands_router
from bot.handlers.lwt_add_media import router as lwt_add_media_router
from bot.handlers.lwt_show_media import router as lwt_show_media_router

router = Router()
router.include_router(commands_router)
router.include_router(auth_router)

router.include_router(lwt_add_media_router)
router.include_router(lwt_show_media_router)
