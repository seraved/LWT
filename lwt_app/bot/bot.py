import logging

from telegram.ext import (
    Application,
    CommandHandler,
)
from lwt_app.core.config import settings


logger = logging.getLogger(__name__)


async def start(update, context):
    await update.message.reply_text("🚀 MediaTracker запущен!")


def run_bot():
    app = Application.builder().token(settings.BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()


if __name__ == "__main__":
    run_bot()
