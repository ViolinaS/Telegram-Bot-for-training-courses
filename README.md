# Шаблон информационного Telegram Бота для школы или курсов

## *A template used as base to run Telegram bots for training courses*

## Основные возможности бота

 ### 1. Администрирование Бота через ``Finite state machine aiogram:``

* Внесение изменений в базу данных (``SQLite``) через интерфейс Telegram.

* Владелец школы(Хозяин бота) сможет сам вносить или удалять информацию о курсах/тренировках, учителях в приложении Telegram.

* Бот осуществляет проверку по ID пользователя.

* Если ID совпадает с ``ID_MASTER``, то будет предоставлен доступ к клавиатуре администратора, в ином случае ---> *Доступ запрещен*

 ### 2. Бот предоставляет пользователю информацию о школе

* Общая информация о школе по кнопке /start, /help

* Общая информация по запросу с клавиатуры:
   1. Кнопка ``Тренировки`` - выводит по порядку все курсы школы.
         * *Информация о каждом курсе содержит: название, фото, описание, продолжительность урока, стоимость урока.*
   2. Кнопка ``Преподаватели`` - выводит по порядку всех учителей школы.
         * *Информация о каждом учителе содержит: ИФО, фото, описание, курс или тренировки, которые ведет учитель*
   3. Кнопка ``Контакты`` - контактная информация
   4. Кнопка ``Режим работы`` - время работы школы

 ### 3. Удаление спама в чатах

* Бот реагирует только на прописанные команды

* Другие сообщения удаляются, Бот предлагает воспользоваться командами на клавиатуре, которые он понимает.

## Запуск Бота

* Установить недостающие пакеты из [requirements.txt](https://github.com/ViolinaS/SalesBot-for-training-courses/blob/main/requirements.txt)

* Создать файл .env и прописать в нем:

  * ``Token`` - токен Бота, полученный у @BotFather в Telegram
  * ``bot_name`` - адрес Бота, полученный у @BotFather в Telegram
  * ``master_id_owner`` - ID Владельца Бота

* Создать группу в Телеграм и пригласить в нее Бота, назначить его администратором.

* Активировать командой ``/moderate`` клавиатуру Администратора

* При первом запуске Бота будет автоматически создана база SQLite, внести первые данные в базу при помощи команд на клавиатуре

 *Важно: команда ``Отмена Загрузки`` отменяет только загрузку (сохранение), а не удаление данных*

****

## Настройки Бота у @BotFather

* Установить через /setjoingroups запрет на добавление Бота в группы

* Установить через /setprivacy статус 'Disable' - (your bot will receive all messages that people send to groups)
