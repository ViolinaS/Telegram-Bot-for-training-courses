from aiogram.utils import executor
from create_bot import dp


async def on_startup(_):
    print('Бот успешно вышел в Телеграм')




executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
