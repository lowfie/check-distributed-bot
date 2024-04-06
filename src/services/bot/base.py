from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from src.config import config


dp = Dispatcher()
bot = Bot(config.bot.token, parse_mode=ParseMode.HTML)
