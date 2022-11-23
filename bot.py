"""Launches the bot"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.config import load_config, Config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user


logger = logging.getLogger(__name__)


def register_all_filters(dp: Dispatcher) -> None:
    """Registers filters"""
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp: Dispatcher) -> None:
    """Registers handlers"""
    register_admin(dp)
    register_user(dp)
    register_echo(dp)


async def main() -> None:
    """Launches the bot"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    config: Config = load_config(path=".env")
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())
    bot["config"] = config

    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
