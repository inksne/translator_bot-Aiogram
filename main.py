from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.utils.chat_action import ChatActionSender
from aiogram.enums.parse_mode import ParseMode
from aiogram.enums.chat_action import ChatAction
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext

from config import BOT_TOKEN
from languages import LanguageSelector
from translate import translate_text_mymemory

import asyncio
import logging

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class Translate(StatesGroup):
    text = State()
    src_lang = State()
    trg_lang = State()
    translated_text = State()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    text = markdown.text(
        f'Приветствую, {markdown.hbold(message.from_user.full_name)}!',
        markdown.text('Я -', markdown.hbold('простой бот переводчик')),
        'Отправьте мне какой-нибудь текст, и я переведу его!',
        'Для просмотра всех команд введите /help',
        sep='\n'
    )
    await message.answer(text=text, parse_mode=ParseMode.HTML)


@dp.message(Command('help'))
async def handle_comands(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    text = markdown.text(
        markdown.hbold('Список всех команд:'),
        '',
        '/start  -  Запуск бота',
        '/help  -  Просмотр всех команд',
        '/cancel  -  Отмена',
        sep='\n'
    )
    await message.answer(text=text, parse_mode=ParseMode.HTML)


@dp.message(Command('cancel'), Translate())
@dp.message(F.text.casefold() == 'cancel', Translate())
async def handle_cancel(message: types.Message, state: FSMContext) -> None:
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    await state.clear()
    await message.answer(text='Отменено.')


@dp.message(default_state)
async def echo_message(message: types.Message, state: FSMContext):
    if message.text:
        await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
        await state.update_data(text=message.text)
        await state.set_state(Translate.src_lang)
        text = markdown.text(
            markdown.hbold('На каком языке этот текст?'),
            markdown.text('Пример ответа: ', markdown.hitalic('русский')),
            sep='\n'
        )
        await message.answer(text=text, parse_mode=ParseMode.HTML)
    else:
        await message.reply(text='Я могу воспринимать только текстовый материал.')


@dp.message(Translate.src_lang, F.text)
async def handle_src_lang(message: types.Message, state: FSMContext):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    if message.text.lower() in LanguageSelector.LANGUAGES:
        await state.update_data(src_lang=LanguageSelector.LANGUAGES[message.text.lower()])
        await state.set_state(Translate.trg_lang)
        text = markdown.text(
            markdown.hbold('На каком языке нужно перевести этот текст?'),
            markdown.text('Пример ответа: ', markdown.hitalic('английский')),
            sep='\n'
        )
        await message.answer(text=text, parse_mode=ParseMode.HTML)
    else:
        await message.answer(text='Язык не найден.')


async def send_result(message: types.Message, data: dict):
    text = markdown.text(
        'Переведенный текст:',
        '',
        markdown.hbold(data['translated_text']),
        markdown.text('Код языка изначального сообщения: ', markdown.hbold(data['src_lang'])),
        markdown.text('Код языка переведённого сообщения: ', markdown.hbold(data['trg_lang'])),
        sep='\n'
    )
    await message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())


@dp.message(Translate.trg_lang, F.text)
async def handle_trg_lang(message: types.Message, state: FSMContext):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    async with ChatActionSender.typing(chat_id=message.chat.id, bot=message.bot):
        if message.text.lower() in LanguageSelector.LANGUAGES:
            await state.update_data(trg_lang=LanguageSelector.LANGUAGES[message.text.lower()])

            data = await state.get_data()
            text_to_translate = data.get('text')
            src_lang = data.get('src_lang')
            trg_lang = data.get('trg_lang')

            translated_text = translate_text_mymemory(
                text=text_to_translate,
                source_lang=src_lang,
                target_lang=trg_lang
            )

            if translated_text:
                await send_result(message, {
                    'translated_text': translated_text,
                    'src_lang': src_lang,
                    'trg_lang': trg_lang
                })
            else:
                await message.answer(text='Произошла ошибка при переводе.')
            await state.clear()
        else:
            await message.answer(text='Язык не найден.')


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        exit(0)