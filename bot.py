    import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# ВСТАВЬ СВОЙ ТОКЕН НИЖЕ
TOKEN = "8330142351:AAFqs9aiWsohW1UIhhb0bzLIRv0Sog4Py9A"

bot = Bot(token=TOKEN)
dp = Dispatcher()

class StoryState(StatesGroup):
    normal_life = State()
    power_discovery = State()
    choice_path = State()

def get_kb(options):
    builder = ReplyKeyboardBuilder()
    for option in options:
        builder.add(types.KeyboardButton(text=option))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def start_story(message: types.Message, state: FSMContext):
    await state.update_data(hero_name=message.from_user.first_name, power_level=0, reputation=0)
    await message.answer(
        f"Обычный понедельник. Ты — обычный подросток, стоишь перед школой. "
        "В кармане последние деньги на обед, а впереди контрольная по физике. Что делаешь?",
        reply_markup=get_kb(["Идти на урок", "Прогулять за школой"])
    )
    await state.set_state(StoryState.normal_life)

@dp.message(StoryState.normal_life, F.text == "Идти on урок")
async def classroom(message: types.Message, state: FSMContext):
    await message.answer(
        "На уроке физики что-то идет не так. Лабораторная установка искрит, "
        "и внезапный разряд бьет прямо в тебя! Ты теряешь сознание..."
    )
    await asyncio.sleep(2)
    await message.answer(
        "Ты проснулся в медпункте. Чувствуешь странный зуд в ладонях. "
        "Взглянув на стакан воды, ты видишь, как он начинает левитировать! Что это?!",
        reply_markup=get_kb(["Попробовать сжать стакан", "Испугаться и убежать"])
    )
    await state.set_state(StoryState.power_discovery)

@dp.message(StoryState.normal_life, F.text == "Прогулять за школой")
async def back_school(message: types.Message, state: FSMContext):
    await message.answer(
        "Ты сидишь за гаражами. Внезапно небо темнеет, и странный метеорит падает "
        "прямо в паре метров от тебя. От него исходит синее свечение...",
        reply_markup=get_kb(["Коснуться свечения", "Сбежать домой"])
    )
    await state.set_state(StoryState.power_discovery)

@dp.message(StoryState.power_discovery)
async def discovery(message: types.Message, state: FSMContext):
    await state.update_data(power_level=10)
    await message.answer(
        "Сила течет по венам. Теперь ты не просто подросток. Ты чувствуешь, "
        "что можешь управлять энергией. Вечером ты видишь, как хулиганы пристают к слабому. "
        "Твой шанс проверить силы!",
        reply_markup=get_kb(["Вмешаться (Сила)", "Пройти мимо", "Проверить статы"])
    )
    await state.set_state(StoryState.choice_path)

@dp.message(F.text == "Проверить статы")
async def check_stats(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        f"📊 Герой: {data['hero_name']}\n"
        f"⚡ Уровень силы: {data['power_level']}\n"
        f"😇 Репутация: {data['reputation']}"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
