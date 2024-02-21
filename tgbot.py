import logging
import asyncio 
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage 

API_TOKEN = '6277925731:AAF7z9HBmgzHDX6ETvVVdHGyKMHaDHELe3o' # Можете создать своего бота, а потом вставить сюда свой токен

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage()) 
dp.middleware.setup(LoggingMiddleware())

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_requests (
        user_id INTEGER PRIMARY KEY,
        status TEXT,
        address TEXT,
        phone_number TEXT
    )
''')
conn.commit()

class YourStateEnum(StatesGroup):
    waiting_for_phone = State()
    waiting_for_address = State()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    logger.info(f"{message.from_user.id} начал взаимодействие с ботом")
    await message.reply("Нұр-Султан қаласының медициналық жедел жәрдем стансасына қош келдіңіз!\n"
                        "Вас приветствует Станция скорой медицинской помощи города Нур-Султан!",
                        parse_mode=ParseMode.MARKDOWN)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Жедел жәрдем шақыру / Вызвать скорую"))
    keyboard.add(types.KeyboardButton("Өтініштің жағдайын тексеру / Проверить статус обращения"))

    await message.reply("Таңдаңыз / Выберите:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Жедел жәрдем шақыру / Вызвать скорую")
async def request_ambulance(message: types.Message):
    logger.info(f"{message.from_user.id} запросил скорую помощь.")
    await message.reply("Нөміріңізді жазыңыз / Напишите ваш номер")

    await YourStateEnum.waiting_for_phone.set()

@dp.message_handler(state=YourStateEnum.waiting_for_phone, content_types=types.ContentTypes.TEXT)
async def process_phone_number(message: types.Message, state: FSMContext):
    raw_phone_number = message.text

    phone_number = ''.join(c for c in raw_phone_number if c.isdigit())

    if len(phone_number) != 11:
        await message.reply("Еңгізілген нөмір дұрыс емес / Напишите номер правильно")
        return

    await state.update_data(phone_number=phone_number)

    await message.reply("Енді адресіңізді жазыңыз! / Теперь напишите свой адрес!")
    await YourStateEnum.waiting_for_address.set()
    
@dp.message_handler(state=YourStateEnum.waiting_for_address, content_types=types.ContentTypes.TEXT)
async def process_address(message: types.Message, state: FSMContext):
    logger.info(f"{message.from_user.id} ввел адрес: {message.text}")
    address = message.text

    data = await state.get_data()
    phone_number = data.get('phone_number')

    # проверка существует ли запись с таким user_id
    cursor.execute("SELECT * FROM user_requests WHERE user_id = ?", (message.from_user.id,))
    existing_data = cursor.fetchone()

    if existing_data:
        # если запись существует, обновляем ее
        cursor.execute('''
            UPDATE user_requests
            SET status = ?, address = ?, phone_number = ?
            WHERE user_id = ?
        ''', ('В обработке', address, phone_number, message.from_user.id))
    else:
        # если записи нет, вставляем новую
        cursor.execute('''
            INSERT INTO user_requests (user_id, status, address, phone_number)
            VALUES (?, ?, ?, ?)
        ''', (message.from_user.id, 'Өңдеуде / В обработке', address, phone_number))

    conn.commit() 

    await message.reply(f"Сіздің адресіңізге жедел жәрдем шақырдық!\nМы вызвали скорую на ваш адрес!\nСіздің / Ваш ID: {message.from_user.id}\nНөмір / Номер: +{phone_number}\nАдрес: {address}")

    await state.finish()
    
@dp.message_handler(lambda message: message.text == "Өтініштің жағдайын тексеру / Проверить статус обращения")
async def check_status(message: types.Message):
    logger.info(f"{message.from_user.id} проверил статус своего обращения.")
    user_id = message.from_user.id
        
    cursor.execute('''
        SELECT * FROM user_requests
        WHERE user_id = ?
    ''', (user_id,))
    data = cursor.fetchone()

    if data:
        status = data[1]  
        address = data[2] 
        phone_number = data[3]  
        await message.reply(f"Сіздің өтінішіңіздің жағдайы:\nВаш статус обращения:\nСіздің / Ваш ID: {user_id}\nЖағдай / Статус: {status}\nАдрес: {address}\nНөмір / Номер: +{phone_number}")
    else:
        await message.reply("Сізде өтініш жоқ.\nУ вас нет активного обращения.")

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(dp.start_polling())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        conn.close()