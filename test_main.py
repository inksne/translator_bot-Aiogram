import pytest
from aiogram import types
from unittest.mock import AsyncMock
from aiogram.fsm.context import FSMContext

from main import handle_start, handle_src_lang, handle_cancel, handle_comands, handle_trg_lang, echo_message, Translate

async def echo(message: types.Message):
    await message.answer(message.text)


@pytest.mark.asyncio
async def test_echo_handler():
    text_mock = "test123"
    message_mock = AsyncMock(text=text_mock)
    await echo(message=message_mock)
    message_mock.answer.assert_called_with(text_mock)


@pytest.mark.asyncio
async def test_handle_start():
    message_mock = AsyncMock(text='/start', from_user=types.User(
        id=123,
        first_name="Test",
        last_name="User",
        username="testuser",
        is_bot=False
    ))
    await handle_start(message=message_mock)
    message_mock.answer.assert_called_once()

    assert "Приветствую" in message_mock.answer.call_args[1]['text']


@pytest.mark.asyncio
async def test_handle_help():
    message_mock = AsyncMock(text='/help', chat=types.Chat(id=123, type="private"))
    await handle_comands(message=message_mock)
    message_mock.answer.assert_called_once()

    assert "Список всех команд" in message_mock.answer.call_args[1]['text']


@pytest.mark.asyncio
async def test_echo_message():
    state_mock = AsyncMock(FSMContext)
    message_mock = AsyncMock(text="Hello")
    await echo_message(message=message_mock, state=state_mock)

    state_mock.update_data.assert_called_with(text="Hello")
    state_mock.set_state.assert_called_with(Translate.src_lang)
    message_mock.answer.assert_called_once()

    assert "На каком языке этот текст?" in message_mock.answer.call_args[1]['text']


@pytest.mark.asyncio
async def test_handle_src_lang():
    state_mock = AsyncMock(FSMContext)
    state_mock.get_data.return_value = {"text": "Привет"}
    message_mock = AsyncMock(text="русский")
    await handle_src_lang(message=message_mock, state=state_mock)

    state_mock.update_data.assert_called_with(src_lang="ru")
    state_mock.set_state.assert_called_with(Translate.trg_lang)
    message_mock.answer.assert_called_once()

    assert "На каком языке нужно перевести этот текст?" in message_mock.answer.call_args[1]['text']


@pytest.mark.asyncio
async def test_handle_trg_lang():
    state_mock = AsyncMock(FSMContext)
    state_mock.get_data.return_value = {
        "text": "Привет",
        "src_lang": "ru",
        "trg_lang": "en"
    }
    message_mock = AsyncMock(text="английский")

    async def translate_mock(*args, **kwargs):
        return "Hello"

    global translate_text_mymemory
    translate_text_mymemory = translate_mock

    await handle_trg_lang(message=message_mock, state=state_mock)
    state_mock.get_data.assert_called_once()
    message_mock.answer.assert_called()
    assert "Переведенный текст:" in message_mock.answer.call_args[1]['text']
    state_mock.clear.assert_called_once()


@pytest.mark.asyncio
async def test_handle_cancel():
    state_mock = AsyncMock(FSMContext)
    message_mock = AsyncMock(text='/cancel', chat=types.Chat(id=123, type="private"))
    await handle_cancel(message=message_mock, state=state_mock)
    state_mock.clear.assert_called_once()
    message_mock.answer.assert_called_once_with(text="Отменено.")