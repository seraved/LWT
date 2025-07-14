
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters
)
from bot.handlers import start, button_handler, handle_add_media
from bot.states import States

from core.config import settings
from utils.logs import logger


def setup_handlers(app: Application):
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            States.ADD_MEDIA: [
                MessageHandler(
                    filters=filters.TEXT & ~filters.COMMAND,
                    callback=handle_add_media,
                )
            ],
            States.MAIN_MENU: [
                CallbackQueryHandler(callback=button_handler)
            ]
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)


def run_bot():
    app = Application.builder().token(settings.BOT_TOKEN).build()
    setup_handlers(app)
    app.run_polling()


if __name__ == "__main__":
    run_bot()
