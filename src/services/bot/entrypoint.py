import asyncio
import logging

from aiogram.types import Message

from src.services.bot.base import dp, bot


async def on_startup() -> None:
    logging.info("Bot started")
    await dp.start_polling(bot)


@dp.message()
async def message_handler(message: Message):
    await message.answer(f"{message.chat.id}")

if __name__ == '__main__':
    asyncio.run(on_startup())
