from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils import callback_answer
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.user import User
from aiogram.filters.command import CommandObject
from aiogram.fsm.context import FSMContext

import random
import re

from states import State, UserState
from db import db_connect
import kb
import text
import config

router = Router()

# Admin commands

@router.message(Command('add_admin'))
async def add_admin(msg: Message, command: CommandObject):
    State.id = msg.from_user.id
    State.first_name = msg.from_user.first_name
    State.last_name = msg.from_user.last_name
    State.is_premium = msg.from_user.is_premium
    State.is_bot = msg.from_user.is_bot

    admin_id_to_check = str(State.id)

    with open('admins_id.txt') as file:
        content = file.read()
        if re.search(r'(?i)' + f'{admin_id_to_check}', content):
            print('Он админ!')
            check = True 
        else:
            await msg.answer('У вас нет доступа к данной команде.')
            print("Он НЕ админ!")
            check = False
            return check

    if check == True:
        True
    else:
        return

    if(command.args is None):
        print("Argument not found")
        await msg.answer(
            'Ошибка: аргументы не переданы.'
        )
        return
    try:
        admin_id = command.args.split(" ", maxsplit=1)
        admin_id = str(admin_id)
        admin_id = admin_id[2:-2]
        if(f'{admin_id}'.isdigit() == True and len(admin_id) > 8):
            pass
        else:
            await msg.answer(
                "Ошибка: неправильный формат команды. Пример:\n"
                "/add_admin [id]"
            )
            return
    except ValueError:
        await msg.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/add_admin [id]"
        )
        return

    with open('admins_id.txt') as file:
        content = file.read()
        if re.search(r'(?i)' + f'{admin_id}', content):
            print('Строка найдена с помощью регулярных выражений!')
            await msg.reply('Ошибка! Этот пользователь уже админ.')
        else:
            print('Строка не найдена!')
            text_to_add = f"{admin_id}"
            with open('admins_id.txt', 'a') as file:
                file.write(text_to_add + '\n')
            await msg.answer(
        
            "Админ добавлен(это тест команды)\n"
            f"Его айди: {admin_id}"
            )


@router.message(Command('help_admin'))
async def list_of_admin_commands(msg: Message):
    State.id = msg.from_user.id
    State.first_name = msg.from_user.first_name
    State.last_name = msg.from_user.last_name
    State.is_premium = msg.from_user.is_premium
    State.is_bot = msg.from_user.is_bot

    admin_id = str(State.id)

    with open('admins_id.txt') as file:
        content = file.read()
        if re.search(r'(?i)' + f'{admin_id}', content):
            print('Строка найдена с помощью регулярных выражений!')
            await msg.reply("""Вот список комманд админа:
1. /add_admin {id}
2. /del_admin {id} (в разработке)
3. /info {id} (в разработке)
4. /ban_user {id} (в разработке)
5. /unban_user {id} (в разработке)
6. /add_clicks_user {id} {количество} (в разработке)
7. /del_clicks_user {id} {количество} (в разработке)
Пока что это всё. По мере работы будут добавляться новые команды, фикситься старые и улучшаться функционал.""")
        else:
            print('Строка не найдена!')
            await msg.reply("У вас нет доступа к этой команде.")
            

@router.message(Command('admin'))
async def admin(msg: Message):
    State.id = msg.from_user.id
    State.first_name = msg.from_user.first_name
    State.last_name = msg.from_user.last_name
    State.is_premium = msg.from_user.is_premium
    State.is_bot = msg.from_user.is_bot

    admin_id = str(State.id)
        

    with open('admins_id.txt') as file:
        content = file.read()
        if re.search(r'(?i)' + f'{admin_id}', content):
            print('Строка найдена с помощью регулярных выражений!')
            await msg.reply("""🌍Приветствую тебя в админ панели.🌏 
Для вывода списка команд напиши \"/help_admin\".""")
        else:
            await msg.reply('У вас нет доступа к этой команде.')

# Main commands

@router.message(Command("start"))
async def start_handler(msg: Message):
    State.id = msg.from_user.id
    State.first_name = msg.from_user.first_name
    State.last_name = msg.from_user.last_name
    State.is_premium = msg.from_user.is_premium
    State.is_bot = msg.from_user.is_bot
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)
    Query = f"""
    INSERT INTO clicks (user_id, total_clicks)
    VALUES
    ({State.id}, 0);
"""
    db_connect(Query)

@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    State.id = msg.from_user.id
    State.first_name = msg.from_user.first_name
    State.last_name = msg.from_user.last_name
    State.is_premium = msg.from_user.is_premium
    State.is_bot = msg.from_user.is_bot
    Query = f"""
    INSERT INTO clicks (user_id, total_clicks)
    VALUES
    ({State.id}, 0);
"""
    db_connect(Query)
    await msg.answer(text.menu, reply_markup=kb.menu)

@router.callback_query(F.data == "click")
async def click(clbck: CallbackQuery):
    State.id = clbck.from_user.id
    State.first_name = clbck.from_user.first_name
    State.last_name = clbck.from_user.last_name
    State.is_premium = clbck.from_user.is_premium
    State.is_bot = clbck.from_user.is_bot
    Query = f"""
    INSERT INTO clicks (user_id, total_clicks)
    VALUES
    ({State.id}, 0);
"""
    db_connect(Query)
    rand_word = random.randint(0, 17)
    if(rand_word == 1):
        word = "тапнули"
    elif(rand_word == 2):
        word = "кликнули"
    elif(rand_word == 3):
        word = "нажали"
    elif(rand_word == 4):
        word = "жмакнули"
    if(rand_word == 5):
        word = "тапнули"
    elif(rand_word == 6):
        word = "кликнули"
    elif(rand_word == 7):
        word = "нажали"
    elif(rand_word == 8):
        word = "жмакнули"
    if(rand_word == 9):
        word = "тапнули"
    elif(rand_word == 10):
        word = "кликнули"
    elif(rand_word == 11):
        word = "нажали"
    elif(rand_word == 12):
        word = "жмакнули"
    if(rand_word == 13):
        word = "тапнули"
    elif(rand_word == 14):
        word = "кликнули"
    elif(rand_word == 15):
        word = "нажали"
    elif(rand_word == 16):
        word = "жмакнули"
    elif(rand_word == 17):
        Query = f"""
UPDATE clicks
SET total_clicks = total_clicks + 100
WHERE user_id = {State.id};
"""
        db_connect(Query)
        word = "получили +100 кликов на счёт(это пасхалка) и ударили по кнопке"
    # await clbck.message.answer(f"{User.id}")
    Query = f"""
UPDATE clicks
SET total_clicks = total_clicks + 1
WHERE user_id = {State.id};
"""
    db_connect(Query)
    Query2 = f"""
SELECT total_clicks FROM clicks
WHERE user_id = {State.id}
"""
    result = db_connect(Query2)
    # print(f"END RESULT: {endResult}")
    result = str(result)
    res_new = result[:-1]
    res_middle = res_new[:-1]
    res_end = res_middle[1:]
    res_end_len = len(res_end)
    res_end_len_minus_1 = res_end_len - 1
    result_end = res_end[res_end_len_minus_1]

    await clbck.message.answer(f"Вы {word} {res_end} раз(-a).")
@router.callback_query(F.data == "balance")
async def balance(clbck: CallbackQuery):
    State.id = clbck.from_user.id
    State.first_name = clbck.from_user.first_name
    State.last_name = clbck.from_user.last_name
    State.is_premium = clbck.from_user.is_premium
    State.is_bot = clbck.from_user.is_bot

    Query2 = f"""
SELECT total_clicks FROM clicks
WHERE user_id = {str(State.id)}
"""
    result = db_connect(Query2)
    result = str(result)
    res_new = result[:-1]
    res_middle = res_new[:-1]
    res_end = res_middle[1:]
    res_end_len = len(res_end)
    res_end_len_minus_1 = res_end_len - 1
    result_end = res_end[res_end_len_minus_1]
    await clbck.message.reply(f"💰 У вас на счету {res_end} кликов. Для обмена в NOT нажмите кнопку на клавиатуре. 💰",  reply_markup=kb.exchange)
@router.message(F.text == "💱 Обменять")
async def exchange(msg: Message, state: FSMContext):
    State.id = msg.from_user.id
    State.first_name = msg.from_user.first_name
    State.last_name = msg.from_user.last_name
    State.is_premium = msg.from_user.is_premium
    State.is_bot = msg.from_user.is_bot
    await state.set_state(UserState.exchange_amount)
    await msg.answer('Напишите количество кликов которое хотите обменять в $NOT: 💱')
    need_message = msg.text
    print(need_message)
    
@router.message(UserState.exchange_amount)
async def exchange_amount_handler(msg: Message, state: FSMContext) -> None:
    amount = msg.text
    print(f"Вы ввели {amount} клика(-ов)?")
    await state.clear()