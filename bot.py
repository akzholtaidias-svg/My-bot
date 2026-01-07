import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# ВСТАВЬ СВОЙ ТОКЕН НИЖЕ
TOKEN = '8330142351:AAFqs9aiWsohW1UIhhb0bzLIRv0Sog4Py9A'

bot = Bot(token=TOKEN)
dp = Dispatcher()

class GameState(StatesGroup):
    step = State()

STORY = {
    "start": {
        "text": "🏰 Ты перед замком на Render! Куда идешь?",
        "options": {"В ворота": "hall", "В сад": "garden"}
    },
    "hall": {
        "text": "🕯 Внутри пусто, но пахнет сыростью. Видишь лестницу.",
        "options": {"Вверх": "win", "Назад": "start"}
    },
    "garden": {
        "text": "🍎 В саду растут золотые яблоки. Одно из них шевелится!",
        "options": {"Съесть": "end", "Уйти": "start"}
    },
    "win": {"text": "🏆 Ты нашел сокровище! ПОБЕДА!", "options": {"Заново": "start"}},
    "end": {"text": "💀 Яблоко было ловушкой... КОНЕЦ.", "options": {"Заново": "start"}}
}

def make_kb(opts):
    b = ReplyKeyboardBuilder()
    for text in opts.keys(): b.button(text=text)
    return b.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(m: types.Message, state: FSMContext):
    await state.set_state(GameState.step)
    await state.update_data(node="start")
    await m.answer(STORY["start"]["text"], reply_markup=make_kb(STORY["start"]["options"]))

@dp.message(GameState.step)
async def handle_game(m: types.Message, state: FSMContext):
    data = await state.get_data()
    curr_node = STORY.get(data.get("node", "start"))
    next_id = curr_node["options"].get(m.text)
    if next_id:
        await state.update_data(node=next_id)
        node = STORY[next_id]
        await m.answer(node["text"], reply_markup=make_kb(node.get("options", {})))

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
