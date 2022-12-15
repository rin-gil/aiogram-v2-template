"""Handles echoes of the message"""

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes, Message

from aiogram.utils.markdown import hcode


async def bot_echo(message: Message) -> None:
    """Echoes on a message with no state"""
    text = ["Эхо без состояния.", "Сообщение:", message.text]
    await message.answer("\n".join(text))


async def bot_echo_all(message: Message, state: FSMContext) -> None:
    """Echoes on the message in state"""
    state_name = await state.get_state()
    text = [f"Эхо в состоянии {hcode(state_name)}", "Содержание сообщения:", hcode(message.text)]
    await message.answer("\n".join(text))


def register_echo(dp: Dispatcher) -> None:
    """Registers message handlers"""
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=ContentTypes.ANY)
