
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters
)
from bot.handlers import media, base, user
from bot.keyboards import constants as kb_val
from bot.states import States

from core.config import settings
from utils.logs import logger


def setup_handlers(app: Application):
    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler("start", base.start)],
    #     states={
    #         States.ADD_MEDIA: [
    #             MessageHandler(
    #                 filters=filters.TEXT & ~filters.COMMAND,
    #                 callback=media.add_media,
    #             )
    #         ],
    #         States.MAIN_MENU: [
    #             CallbackQueryHandler(callback=media.button_handler)
    #         ],
    #         States.VIEWING_LIST: [
    #             CallbackQueryHandler(
    #                 media.toggle_watch_handler, pattern=r"^toggle_watch_\d+$"),
    #             CallbackQueryHandler(media.page_handler, pattern="^page_\d+$"),
    #             CallbackQueryHandler(base.back_to_menu, pattern="^main_menu$")
    #         ]
    #     },
    #     fallbacks=[CommandHandler("cancel", base.back_to_menu)]
    # )
    lwt_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", base.start)],
        states={
            States.START_MENU: [
                # Авторизация и главное меню
                MessageHandler(
                    filters=filters.CONTACT,
                    callback=user.auth_user,
                ),
                MessageHandler(
                    filters=filters.ALL,
                    callback=base.start,
                )
            ],
            States.MAIN_MENU: [
                MessageHandler(
                    filters=filters.Regex(kb_val.ADD_CONTENT_TEXT),
                    callback=media.adding_media,
                ),
                MessageHandler(
                    filters=filters.Regex(kb_val.SHOW_CONTENT_TEXT),
                    callback=media.showing_media,
                ),
                MessageHandler(
                    filters=filters.ALL,
                    callback=base.main_menu,
                )
            ],
            # ADD MEDIA
            States.CHOOSING_MEDIA_TYPE: [
                CallbackQueryHandler(
                    callback=media.get_media_type,
                    pattern=f"^{kb_val.KEY_ANIME_ADD}$",
                ),
                CallbackQueryHandler(
                    callback=media.get_media_type,
                    pattern=f"^{kb_val.KEY_MOVIE_ADD}$",
                ),
                CallbackQueryHandler(
                    callback=media.get_media_type,
                    pattern=f"^{kb_val.KEY_SERIES_ADD}$",
                ),
            ],
            States.SAVE_MEDIA: [
                MessageHandler(
                    filters=filters.TEXT & ~filters.COMMAND,
                    callback=media.save_media,
                ),
                CallbackQueryHandler(
                    callback=media.go_back_to_add_media,
                    pattern=f"^{kb_val.KEY_BACK_TO_ADD_MEDIA}$",
                ),
            ],
            # SHOW MEDIA
            States.START_SHOW_MEDIA: [

            ]

            # States.START_ADD_MEDIA: [
            #     CallbackQueryHandler(callback=media.button_handler),
            #     CallbackQueryHandler(
            #         callback=base.back_to_menu,
            #         pattern=f"^{kb_val.KEY_MAIN_MENU}$",
            #     )
            # ],

            # States.ADDING_SERIES_DETAILS: [
            #     MessageHandler(filters.TEXT & ~filters.COMMAND, save_series)
            # ]
            # States.SHOW_MEDIA: [
            #     # CallbackQueryHandler(
            #     #     media.toggle_watch_handler, pattern=r"^toggle_watch_\d+$"),
            #     # CallbackQueryHandler(media.page_handler, pattern="^page_\d+$"),
            #     CallbackQueryHandler(
            #         callback=base.back_to_menu,
            #         pattern=f"^{kb_val.KEY_MAIN_MENU}$",
            #     )
            # ]
        },
        fallbacks=[
            CommandHandler('start', base.start),
            MessageHandler(filters.ALL, base.start)
        ],
    )

    app.add_handler(lwt_conv_handler)


def run_bot():
    app = Application.builder().token(settings.BOT_TOKEN).build()
    setup_handlers(app)
    app.run_polling()


if __name__ == "__main__":
    run_bot()
