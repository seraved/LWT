import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # logging.FileHandler("./logs/bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
