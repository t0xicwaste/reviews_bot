from aiogram import Router, F

from aiogram.types import Message
from aiogram.filters import CommandStart

from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext
from FSM.state import Reviews

from keyboards import review_kb as kb
from dict.dict_review import GRADE, GUEST, THEME, NEXT_THEME, NEXT_REVIEW

router = Router()

# functions grades
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer_sticker("CAACAgIAAxkBAAENFNJnK-R3_V77DEVPnQQF46CglHasSgACvUAAAuVzYEqLNc48PMgD8TYE")
    await message.answer("Привет! Спасибо за посещение дискуссионного клуба! Наша команда надеется, что эта встреча вам понравилась.")
    await message.answer(text='Пожалуйста, оставьте свой отзыв с впечатлениями от встречи: ')
    await message.answer(text='Оцените от 1 до 10 прошедшую встречу', reply_markup=kb.grade)
    await state.set_state(Reviews.grade)

@router.callback_query(F.data.in_(['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']), Reviews.grade)
async def input_guest(callback: CallbackQuery, state: FSMContext):
    await state.update_data(grade=callback.data)
    await callback.message.answer(text='Готовы ли вы пригласить друзей в наш дискуссионный клуб на следующие встречи?', reply_markup=kb.guest)
    await state.set_state(Reviews.guest)

@router.callback_query(F.data.in_(['yes', 'no', 'maybe']), Reviews.guest)
async def input_theme(callback: CallbackQuery, state: FSMContext):
    await state.update_data(guest=callback.data)
    await callback.message.answer(text='Понравилась ли вам тема нашей встречи?', reply_markup=kb.theme)
    await state.set_state(Reviews.theme)

@router.callback_query(F.data.in_(['very', 'fifty', 'notvery']), Reviews.theme)
async def input_next_theme(callback: CallbackQuery, state: FSMContext):
    await state.update_data(theme=callback.data)
    await callback.message.answer(text='Какую бы тему вы хотели видеть в следующий раз?', reply_markup=kb.next_theme)
    await state.set_state(Reviews.next_theme)

# Функция обработки ввода сообщений и нажатия на кнопку далее для оценки темы
@router.message(Reviews.next_theme)
@router.callback_query(F.data.in_(['next_theme']))
async def input_next_review_and_final_theme(event: CallbackQuery | Message, state: FSMContext):
    if isinstance(event, CallbackQuery):
        await state.update_data(next_theme=event.data)
    elif isinstance(event, Message):
        await state.update_data(next_theme=event.text)
    await (event.message if isinstance(event, CallbackQuery) else event).answer(text='Здесь вы можете написать все свои предложения/желания/критику', reply_markup=kb.next_review)
    await state.set_state(Reviews.next_review)

# Функция обработки ввода сообщений и нажатия на кнопку далее для отзыва
@router.message(Reviews.next_review)
@router.callback_query(F.data.in_(['next_review']))
async def input_next_review(event: CallbackQuery | Message, state: FSMContext):
    if isinstance(event, CallbackQuery):
        await state.update_data(next_review=event.data)
    elif isinstance(event, Message):
        await state.update_data(next_review=event.text)
    user_data = await state.get_data()

    formatted_review = f"""
    Ваш отзыв:
    Оценка встречи: {GRADE.get(user_data.get('grade'), 'Не указана')}
    Пригласили бы друзей: {GUEST.get(user_data.get('guest'), 'Не указано')}
    Тема встречи: {THEME.get(user_data.get('theme'), 'Не указана')}
    Следующая тема: {NEXT_THEME.get(user_data.get('next_theme'), 'Не указана')}
    Дополнительный отзыв: {NEXT_REVIEW.get(user_data.get('next_review'), 'Не указан')}
    """

    # Отправка итогового сообщения
    await (event.message if isinstance(event, CallbackQuery) else event).answer(text=formatted_review)
    # await (event.message if isinstance(event, CallbackQuery) else event).answer(text='Спасибо за ваш отзыв!\n#ямыменяться')

    await state.clear()