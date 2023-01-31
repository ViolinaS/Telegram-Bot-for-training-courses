from handlers import client, manage
from aiogram.utils import executor
from create_bot import dp


async def on_startup(_):
    print('Бот успешно вышел в Телеграм')


#client.register_handlers_client(dp)
#manage.register_handlers_manage(dp)
client.handlers_register(dp)
manage.handlers_register(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
