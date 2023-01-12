from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from regard_parser import categories_dict

# Создаем CallbackData-объекты, которые будут нужны для работы с менюшкой
menu_cd = CallbackData("show_menu", "level", "category", "subcategory", "item_id")
buy_item = CallbackData("buy", "item_id")

# С помощью этой функции будем формировать коллбек дату для каждого элемента меню, в зависимости от
# переданных параметров. Если Подкатегория, или айди товара не выбраны - они по умолчанию равны нулю
def make_callback_data(level, category="0", subcategory="0", item_id="0"):
    return menu_cd.new(level=level, category=category, subcategory=subcategory, item_id=item_id)


async def categories_keyboard(): #async  создает кнопки, берет их из списка категорий, пока одна категория(Видеокарты)
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup()
    categories = [i for i in categories_dict.values()]
    for category in categories:
        button_text = category
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category)
        markup.insert(InlineKeyboardButton(text=button_text, callback_data=callback_data))
    return markup

async def subcategories_keyboard(category):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(InlineKeyboardButton(text='Продолжить', callback_data=make_callback_data(level=10)))
    markup.row(InlineKeyboardButton(text='Фильтр', callback_data=make_callback_data(level=CURRENT_LEVEL + 1)))
    markup.row(InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1)))
    return markup

async def filter_categories_keyboard(category):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)
    filter_buttons = ['💰 Цена', '💾 Память', '💻 Производитель']
    for button in filter_buttons:
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category)
        markup.insert(InlineKeyboardButton(text=button, callback_data=callback_data))
    markup.row(InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1)))
    return markup

async def price(category):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text='Назад', callback_data=make_callback_data(level=2, category=category)))



'''
Нужно распарсить данные по категориям и потом уже доделать кнопки. Образец по кнопкам по ссылке:
https://github.com/Latand/telegram-bot-lessons/blob/master/lesson-7/keyboards/inline/menu_keyboards.py
'''