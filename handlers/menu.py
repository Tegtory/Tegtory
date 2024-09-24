from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import URLInputFile

from Filters import MenuFilter
from MIddleWares.ChatActionMiddleWare import Typing
from States import FindFactory
from bot import bot
from config import not_enough_points, factory_image
from api import api
from replys import menu_reply, mini_game_markup, city_markup

router = Router()
router.message.middleware(Typing())


city_text = 'Вы в центре города'
mini_games_text = ('''
🎮 Мини игры 🎮

🌾 *Ферма:* ежедневный бонус 

⚔️ *Инспекция:*
Инспектор сравнит твою фабрику с фабрикой другого игрока и добавить тебе рейтинг

🎲 *Биржа:*
Вложитесь в товар и узнайте выростет ли он в цене

🎲 *Казино:* @an\_casino\_bot
''')


@router.message(MenuFilter())
async def menu_cmd(message: types.Message):
    await message.answer(f'Привет {message.from_user.first_name}.', reply_markup=menu_reply)


@router.callback_query(F.data == 'city')
async def back_city(call: types.CallbackQuery):
    await call.message.edit_text(city_text, reply_markup=city_markup)


@router.message(F.text.lower() == 'город')
async def city(message: types.Message):
    await message.answer(city_text, reply_markup=city_markup)


@router.message(F.text.lower() == 'мини игры')
async def mini_games_menu(message: types.Message):
    await message.answer(mini_games_text, reply_markup=mini_game_markup, parse_mode='Markdown')


@router.message(F.text.lower() == 'помощь')
async def guide(message: types.Message):
    await message.answer('Гайд со всем необходимым: https://telegra.ph/Obuchenie-Tegtory-08-30')


@router.message(F.text.lower() == 'найти')
async def find_factory(message: types.Message, state: FSMContext):
    await state.set_state(FindFactory.name)
    await message.answer('Напишите название фабрики которую хотите найти')


@router.message(StateFilter(FindFactory.name))
async def answer_found_factory(message: types.Message, state: FSMContext):
    factory = api.find_factory(message.text)
    if not factory.exists():
        return await message.answer('Фабрика не найдена')
    _type = factory_image(factory.type)
    await message.answer_photo(URLInputFile(_type),
                               f'*{factory.name}:* \n\n'
                               f'🔧 *{factory.lvl} уровень*\n'
                               f'⚙️ *Тип {factory.type}* \n'
                               f'🚧 *Статус {'Не работает' if factory.state == 0 else 'Работает'}*  \n'
                               f'👷‍ *{factory.workers} работников* ')
    await state.clear()


@router.message(F.text.lower().split()[0] == 'передать')
async def give_money(message: types.Message):
    try:
        _id = str(message.text.split()[1])
        _money = abs(int(message.text.split()[2]))
        player = api.player(message.from_user.id)
    except:
        return await message.answer('Принцип передачи денег: передать @username 1203')
    if _money > player.money:
        return await message.answer(not_enough_points)
    try:
        player2 = api.player(_id)
        player2.money += _money
        player.money -= _money
    except:
        return await message.answer('видимо вы неверно указали username')

    await bot.send_message(player2.telegram_id, f'Вам передали {int(_money):,}')
    await message.answer(f'Успешно')
    await bot.send_message(1405684214, f'кому {_id} {_money} от {message.from_user.username}')
