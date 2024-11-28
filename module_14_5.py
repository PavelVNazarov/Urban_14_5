# Проверить как функции is_included и add_user правильно реализованы в Вашем модуле crud_functions





from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import sqlite3

# Подключение к базе данных
connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

# Токен бота
api = '7890006550:AAG_yy6ORoAvP2CCfkZ_vnM8HQfHbDzBHvQ'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Клавиатуры
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button3 = KeyboardButton(text='Рассчитать')
button4 = KeyboardButton(text='Информация')
button5 = KeyboardButton(text='Купить')
button6 = KeyboardButton(text='Регистрация')
kb.row(button3, button4, button5, button6)

kb1 = InlineKeyboardMarkup(resize_keyboard=True)
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb1.row(button, button2)

kb2 = InlineKeyboardMarkup(resize_keyboard=True)
products = ['Product1', 'Product2', 'Product3', 'Product4']
for product in products:
    kb2.add(InlineKeyboardButton(product, callback_data='product_buying'))

# Состояния
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

@dp.message_handler(text='Регистрация')
async def sign_up(message):
    await message.answer('Введите имя пользователя (только латинские буквы)')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    is_inc = is_included(message.text)  # Функция для проверки уникальности имени пользователя
    if is_inc:
        await message.answer('Данное имя уже занято, введите другое')
    else:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email')
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await RegistrationState.age.set()
    await message.answer('Введите свой возраст:')

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    user_data = await state.get_data()
    add_user(user_data["username"], user_data["email"], user_data["age"])  # Функция для добавления пользователя в базу
    await message.answer('Регистрация прошла успешно', reply_markup=kb1)
    await state.finish()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Информация о боте!')

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb1)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(1, 5):
        await message.answer(f'Название: {products[i-1]} | Описание: Описание {i} | Цена: {i*100}')
        with open(f'{i}.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer("Выберите продукт для покупки:", reply_markup=kb2)

@dp.callback_query_handler(text=['product_buying'])
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def calculate_calories(call):
    await call.message.answer('Введите Ваш вес (кг):')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def get_weight(message, state):
    weight = float(message.text)
    await state.update_data(weight=weight)

    await message.answer('Введите Ваш рост (см):')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def get_growth(message, state):
    growth = float(message.text)
    await state.update_data(growth=growth)

    await message.answer('Введите Ваш возраст (годы):')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def calculate(message, state):
    age = int(message.text)
    user_data = await state.get_data()
    weight = user_data["weight"]
    growth = user_data["growth"]

    # Расчет калорий по формуле
    calories = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f'Ваша норма калорий: {calories:.2f}')
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
