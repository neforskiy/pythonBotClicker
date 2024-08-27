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

from utils import *
from states import UserState, ExchangeState
from db import db_connect
import kb
import text
import config

router = Router()

# Admin commands

@router.message(Command('add_admin'))
async def add_admin(msg: Message, command: CommandObject):
    UserState.id = msg.from_user.id
    UserState.first_name = msg.from_user.first_name
    UserState.last_name = msg.from_user.last_name
    UserState.is_premium = msg.from_user.is_premium
    UserState.is_bot = msg.from_user.is_bot

    admin_id_to_check = str(UserState.id)

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
    UserState.id = msg.from_user.id
    UserState.first_name = msg.from_user.first_name
    UserState.last_name = msg.from_user.last_name
    UserState.is_premium = msg.from_user.is_premium
    UserState.is_bot = msg.from_user.is_bot

    admin_id = str(UserState.id)

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
    UserState.id = msg.from_user.id
    UserState.first_name = msg.from_user.first_name
    UserState.last_name = msg.from_user.last_name
    UserState.is_premium = msg.from_user.is_premium
    UserState.is_bot = msg.from_user.is_bot

    admin_id = str(UserState.id)
        

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
    UserState.id = msg.from_user.id
    UserState.first_name = msg.from_user.first_name
    UserState.last_name = msg.from_user.last_name
    UserState.is_premium = msg.from_user.is_premium
    UserState.is_bot = msg.from_user.is_bot
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)
    Query = f"""
    INSERT INTO clicks (user_id, total_clicks)
    VALUES
    ({UserState.id}, 0);
"""
    db_connect(Query)

@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    UserState.id = msg.from_user.id
    UserState.first_name = msg.from_user.first_name
    UserState.last_name = msg.from_user.last_name
    UserState.is_premium = msg.from_user.is_premium
    UserState.is_bot = msg.from_user.is_bot
    Query = f"""
    INSERT INTO clicks (user_id, total_clicks)
    VALUES
    ({UserState.id}, 0);
"""
    db_connect(Query)
    await msg.answer(text.menu, reply_markup=kb.menu)

@router.callback_query(F.data == "click")
async def click(clbck: CallbackQuery):
    UserState.id = clbck.from_user.id
    UserState.first_name = clbck.from_user.first_name
    UserState.last_name = clbck.from_user.last_name
    UserState.is_premium = clbck.from_user.is_premium
    UserState.is_bot = clbck.from_user.is_bot
    Query = f"""
    INSERT INTO clicks (user_id, total_clicks)
    VALUES
    ({UserState.id}, 0);
"""
    db_connect(Query)

    Query1 = f"""
UPDATE clicks
SET total_clicks = total_clicks + 1
WHERE user_id = {UserState.id};
"""
    db_connect(Query1)
    Query2 = f"""
SELECT total_clicks FROM clicks
WHERE user_id = {UserState.id}
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

    await clbck.message.answer(f"Вы кликнули {res_end} раз(-a).")
@router.callback_query(F.data == "balance")
async def balance(clbck: CallbackQuery):
    UserState.id = clbck.from_user.id
    UserState.first_name = clbck.from_user.first_name
    UserState.last_name = clbck.from_user.last_name
    UserState.is_premium = clbck.from_user.is_premium
    UserState.is_bot = clbck.from_user.is_bot

    Query1 = f"""
SELECT total_NOT FROM NOTs
WHERE user_id = {str(UserState.id)}
"""

    Query2 = f"""
SELECT total_clicks FROM clicks
WHERE user_id = {str(UserState.id)}
"""
    result2 = db_connect(Query1)
    amount_NOT = await Delete1stAndLastAndPreLastSymbolFromDBsQuery(result2)
    result = db_connect(Query2)
    result = str(result)
    res_new = result[:-1]
    res_middle = res_new[:-1]
    res_end = res_middle[1:]
    res_end_len = len(res_end)
    res_end_len_minus_1 = res_end_len - 1
    result_end = res_end[res_end_len_minus_1]
    await clbck.message.reply(f"💰 У вас на счету {res_end} кликов и {amount_NOT} NOT. Если желаете обменять в NOT нажмите кнопку на клавиатуре. 💰",  reply_markup=kb.exchange)
@router.message(F.text == "💱 Обменять")
async def exchange(msg: Message, state: FSMContext):
    UserState.id = msg.from_user.id
    UserState.first_name = msg.from_user.first_name
    UserState.last_name = msg.from_user.last_name
    UserState.is_premium = msg.from_user.is_premium
    UserState.is_bot = msg.from_user.is_bot
    await state.set_state(ExchangeState.exchange_amount)
    await msg.answer('Напишите количество кликов которое хотите обменять в $NOT: 💱')

@router.callback_query(F.data == "exchange")
async def exchangeCLBCK(clbck: CallbackQuery, state: FSMContext):
    UserState.id = clbck.from_user.id
    UserState.first_name = clbck.from_user.first_name
    UserState.last_name = clbck.from_user.last_name
    UserState.is_premium = clbck.from_user.is_premium
    UserState.is_bot = clbck.from_user.is_bot
    await state.set_state(ExchangeState.exchange_amount)
    await clbck.message.answer('Напишите количество кликов которое хотите обменять в $NOT: 💱')

@router.message(ExchangeState.exchange_amount)
async def exchange_amount_handler(msg: Message, state: FSMContext) -> None:
    UserState.id = msg.from_user.id
    UserState.first_name = msg.from_user.first_name
    UserState.last_name = msg.from_user.last_name
    UserState.is_premium = msg.from_user.is_premium
    UserState.is_bot = msg.from_user.is_bot
    amount = msg.text
    QuerySELall = f"""
SELECT total_clicks FROM clicks
WHERE user_id = {str(UserState.id)}
"""
    result = db_connect(QuerySELall)
    result = str(result)
    res_new = result[:-1]
    res_middle = res_new[:-1]
    res_end = res_middle[1:]
    res_end = int(res_end)
    amount = int(amount)
    if(amount > res_end):
        await msg.reply("Вы ввели число больше, чем у вас кликов!")
    elif(amount <= res_end):
        QueryToNOT1 = f"""
UPDATE clicks
SET total_clicks = total_clicks - {amount}
WHERE user_id = {str(UserState.id)}
"""
    amount_NOT = amount * 0.00002
    amount_NOT = str(amount_NOT)
    amount_NOT = amount_NOT[:-10]
    QueryToCheckDBs = f"""
SELECT user_id from NOTs
WHERE user_id = {str(UserState.id)}
"""
    checkDBs = db_connect(QueryToCheckDBs)
    checkDBs = str(checkDBs)
    if(checkDBs == "None"):
        Query = f"""
INSERT INTO NOTs (user_id, total_NOT)
VALUES
({str(UserState.id)}, 0)
"""
        db_connect(Query)
    else:
        # checkDBs = str(checkDBs)
        # checkDBs_new = checkDBs[:-1]
        # checkDBs_middle = checkDBs_new[:-1]
        # checkDBs_end = checkDBs_middle[1:]
        # checkDBs_end = str(checkDBs_end)
#         QueryNew = f"""
# UPDATE `NOTs`
# SET `total_NOT` = `total_NOT` + {amount_NOT}
# WHERE `NOTs`.`user_id` = {str(UserState.id)};
# """
        db_connect(QueryToNOT1)
        QueryNew = """
UPDATE `NOTs` 
SET `total_NOT` = `total_NOT` + 97.323960000000000000000000000000
WHERE `NOTs`.`total_NOT` = "1265852777";
"""
        db_connect(QueryNew)
        await msg.reply("Успешно!")
    
    await state.clear()