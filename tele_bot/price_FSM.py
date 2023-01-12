from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp


class FSMPrice(StatesGroup):
    min_price = State()
    max_price = State()


async def min_price(message: types.Message):
    await FSMPrice.min_price.set()
    await message.reply('Введите минимальную цену: ')


async def save_min_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['min'] = message.text
    await FSMPrice.next()
    await message.reply('Введите предельную цену: ')


async def save_max_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['max'] = message.text

    get_data = await state.get_data()
    await message.reply(get_data)
    await state.finish()

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(min_price, state=None)
    dp.register_message_handler(save_min_price, state=FSMPrice.min_price)
    dp.register_message_handler(save_max_price, state=FSMPrice.max_price)
