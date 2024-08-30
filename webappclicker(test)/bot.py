import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import  Command
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sys

def webapp_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🚀 Let's click!", web_app=WebAppInfo(
            url="https://dymdngj5sa.eu.loclx.io"
        )
    )
    return builder.as_markup()

router = Router()

@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.reply("Click! Click! Click!", reply_markup=webapp_builder())

async def main():
    bot = Bot(token="6880969982:AAEkVx7LagpVGF60zAbBEd033kpROjs8WC0", default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())