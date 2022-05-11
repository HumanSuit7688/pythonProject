from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
storage = MemoryStorage()


from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

available_coffee_names = ["americano", "latte", "cappuccino"]
available_cup_sizes = ["small", "medium", "big"]
available_deserts_names = ["чизкейк", "мороженное", "пирог",]
available_deserts_sizes = ["средний", "большой"]

class OrderCoffe(StatesGroup):
    waiting_for_coffee_name = State()
    waiting_for_cup_size = State()
    waiting_for_deserts_name = State()
    waiting_for_deserts_size = State()

@dp.message_handler(commands="coffe", state="*")
async def coffee_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_coffee_names:
        keyboard.add(name)
    await message.answer("Выберите кофе:", reply_markup=keyboard)
    await OrderCoffe.waiting_for_coffee_name.set()


@dp.message_handler(state=OrderCoffe.waiting_for_coffee_name)
async def coffee_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_coffee_names:
        await message.answer("Пожалуйста, выберите кофе, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_food=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_cup_sizes:
        keyboard.add(size)
    await OrderCoffe.next()
    await message.answer("Теперь выберите размер порции:", reply_markup=keyboard)


@dp.message_handler(state=OrderCoffe.waiting_for_cup_size)
async def coffee_size_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_cup_sizes:
        await message.answer("Пожалуйста, выберите размер порции, используя клавиатуру ниже.")
        return
    user_data = await state.get_data()
    await message.answer(f"Вы заказали {message.text.lower()} порцию {user_data['chosen_food']}.\n"
                         f"Попробуйте теперь заказать десерты: /deserts", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

@dp.message_handler(commands="deserts, state="*")
async def coffee_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_deserts_names:
        keyboard.add(name)
    await message.answer("Выберите десерт:", reply_markup=keyboard)
    await OrderCoffe.waiting_for_deserts_name.set()

@dp.message_handler(state=OrderCoffe.waiting_for_deserts_name)
async def coffee_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_coffee_names:
        await message.answer("Пожалуйста, выберите десерт, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_food=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_deserts_sizes:
        keyboard.add(size)
    await OrderCoffe.next()
    await message.answer("Теперь выберите размер порции:", reply_markup=keyboard)

@dp.message_handler(state=OrderCoffe.waiting_for_deserts_size)
async def coffee_size_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_deserts_sizes:
        await message.answer("Пожалуйста, выберите размер порции, используя клавиатуру ниже.")
        return
    user_data = await state.get_data()
    await message.answer(f"Вы заказали {message.text.lower()} порцию {user_data['chosen_food']}.\n", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
if __name__ == '__main__':
    executor.start_polling(dp)
