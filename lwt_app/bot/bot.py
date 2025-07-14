
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters
)
from bot.handlers import media, base
from bot.states import States

from core.config import settings
from utils.logs import logger


def setup_handlers(app: Application):
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", base.start)],
        states={
            States.ADD_MEDIA: [
                MessageHandler(
                    filters=filters.TEXT & ~filters.COMMAND,
                    callback=media.add_media,
                )
            ],
            States.MAIN_MENU: [
                CallbackQueryHandler(callback=media.button_handler)
            ],
            States.VIEWING_LIST: [
                CallbackQueryHandler(media.page_handler, pattern="^page_\d+$"),
                CallbackQueryHandler(base.back_to_menu, pattern="^main_menu$")
            ]
        },
        fallbacks=[CommandHandler("cancel", base.back_to_menu)]
    )

    app.add_handler(conv_handler)


def run_bot():
    app = Application.builder().token(settings.BOT_TOKEN).build()
    setup_handlers(app)
    app.run_polling()


if __name__ == "__main__":
    run_bot()
