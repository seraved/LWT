import asyncio

from bot.bot import main
from utils.logs import logger

if __name__ == "__main__":
    logger.info("Start")
    asyncio.run(main())
