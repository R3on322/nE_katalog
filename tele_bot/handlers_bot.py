import time
from typing import Union
from aiogram import Dispatcher, types
from aiogram.types import CallbackQuery, Message
from keyboards.keyboard_bot import categories_keyboard, subcategories_keyboard, menu_cd, filter_categories_keyboard
from create_bot import dp
from price_FSM import min_price


@dp.message_handler(commands='start')
async def show_menu(message: types.Message):
    await list_categories(message)

async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    markup = await categories_keyboard()
    if isinstance(message, Message):
        await message.answer('нЕ-каталог, бот с ценами на товары популярных сайтов', reply_markup=markup)
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)

async def list_subcategories(callback: CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category)
    await callback.message.edit_reply_markup(markup)

async def list_filter_categories(callback: CallbackQuery, category, **kwargs):
    markup = await filter_categories_keyboard(category)
    await callback.message.edit_reply_markup(markup)

async def list_items(callback: CallbackQuery, category):
    await callback.message.answer('Пожалуйста, подождите 🫠')
    time.sleep(1)
    with open(f'data/mvideo_pars/Видеокарты.json', encoding='UTF-8') as file:
        prod_data = json.load(file)
    for product in prod_data:
        card = f"{hlink(product.get('NAME'), product.get('URL'))}\n" \
               f"{hbold('Цена: ')}{product.get('PRICE')} ₽"
        await callback.message.answer(card)
        time.sleep(1)

async def price_from_user(callback: CallbackQuery, category, subcategory):
    await min_price(message=callback.message)
    user_price = callback.message.values   # НАДО КАК ТО ПОЛУЧИТЬ ДАННЫЕ ИЗ FSM
    print(user_price)

@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    category = callback_data.get("category")
    subcategory = callback_data.get("subcategory")
    levels = {
        "0": list_categories,  # Отдаем категории
        "1": list_subcategories,  # Отдаем Фильтр и Продолжить
        "2": list_filter_categories, # Отдаем подкатегории Фильтра
        "3": price_from_user, #Ждем диапозон цен от пользователя
        "10": list_items,
    }
    current_level_function = levels[current_level]
    await current_level_function(
        call,
        category=category,
        subcategory=subcategory,
    )

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(show_menu, commands=['start'])