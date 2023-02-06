from create_bot import dp, bot, client_commands, Dispatcher
from aiogram import types

 
#@dp.message_handler() # Фильтрация спама и мата в чате клиентской части
async def clean_chat(message: types.Message):
     if message.text not in client_commands:
         await message.delete()
         await bot.send_message(message.from_user.id, 'Бот Вас не понял, пожалуйста воспользуйтесь командами на клавиатуре')
         
         
def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(clean_chat)