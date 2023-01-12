from aiogram.utils import executor
from create_bot import dp


def main():
    import handlers_bot, price_FSM

    handlers_bot.register_handlers(dp)
    price_FSM.register_handlers_admin(dp)

    executor.start_polling(dp, skip_updates=True)

if __name__=='__main__':
    main()