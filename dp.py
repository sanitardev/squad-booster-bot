from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from utils import DB
from filters import *

db = DB()
storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(IsBotAdminFilter)
dp.filters_factory.bind(IsBotRestrictFilter)
dp.filters_factory.bind(MemberCanRestrictFilter)
dp.filters_factory.bind(IsCallAdminFilter)


