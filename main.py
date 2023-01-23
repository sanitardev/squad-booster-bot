from dp import dp
from aiogram.utils import executor
import handlers


if __name__ == '__main__':
    print("Bot strated")
    executor.start_polling(dp, skip_updates=True, on_startup=handlers.chat_handlers.on_startup)

