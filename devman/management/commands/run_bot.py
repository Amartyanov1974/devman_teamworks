from datetime import time

from django.core.management import BaseCommand
from django.conf import settings
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
)

from devman.models import Student


TIMESLOTS = [
    '16',
    '17',
    '18',
    '19',
    '20',
    '21',
]


def start(update: Update, context: CallbackContext):
    context.user_data['start_time'] = TIMESLOTS[0]
    context.user_data['end_time'] = TIMESLOTS[-1]
    text = (
        'Привет, наступает пора командных проектов. '
        'Будет вместо учебного плана. '
        'Будет что-то вроде урока на девмане, только без шагов, '
        'зато втроём (очень редко вдвоем) + с ПМом. '
        'Созвоны будут по 20 минут каждый день в течение недели. '
        'Быть у компьютера не обязательно.'
    )
    picture = (
        'https://s39613.pcdn.co/wp-content/uploads/2014/09/'
        'iStock-516797126.jpg'
    )
    button = InlineKeyboardButton(
        text='Указать временные возможности', callback_data='SHOW_TIME_VIEW'
    )
    keyboard = InlineKeyboardMarkup([[button]])
    update.message.reply_photo(picture, text, reply_markup=keyboard)

    return 'EXPECTING_CONTINUATION'


def show_time_view(update: Update, context: CallbackContext):
    update.callback_query.answer()

    picture = (
        'https://images.theconversation.com/files/401267/original/'
        'file-20210518-13-1a2rmfe.jpg'
    )

    start_time = context.user_data.get('start_time')
    end_time = context.user_data.get('end_time')
    caption = (
        'Выберите удобное время для созвонов.\n'
        f'Выбранное время: {start_time}-{end_time}.'
    )
    buttons = [
        [InlineKeyboardButton('Изменить', callback_data='SET_SPAN')],
        [InlineKeyboardButton('Готово', callback_data='CONFIRMATION')],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.message.reply_photo(
        picture,
        caption,
        reply_markup=keyboard,
    )
    return 'SELECTING_OPTION'


def select_time_asd(update: Update, context):
    update.callback_query.answer()
    timeslots = [
        '17:00',
        '18:00',
        '19:00',
        '20:00',
        '21:00',
    ]
    buttons = [
        [InlineKeyboardButton(timeslot, callback_data=timeslot)]
        for timeslot in timeslots
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.message.reply_photo(
        'Выберите удобное время для созвонов',
        reply_markup=keyboard,
    )
    return 'SELECTING_TIME'


def ask_which_span_part_to_set(update: Update, context: CallbackContext):
    update.callback_query.answer()

    start_time = context.user_data.get('start_time')
    end_time = context.user_data.get('end_time')
    caption = (
        'Выберите удобное время для созвонов\n'
        f'Выбранное время: {start_time}-{end_time}'
    )
    buttons = [
        [
            InlineKeyboardButton(
                'Начало периода', callback_data='SET_START_TIME'
            )
        ],
        [InlineKeyboardButton('Конец периода', callback_data='SET_END_TIME')],
        [InlineKeyboardButton('Вернуться', callback_data='RETURN')],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.message.edit_caption(caption, reply_markup=keyboard)
    return 'SELECTING_WHAT_PART_TO_CHANGE'


def select_hour(update: Update, context: CallbackContext):
    update.callback_query.answer()

    start_time = context.user_data.get('start_time')
    end_time = context.user_data.get('end_time')
    caption = (
        'Выберите удобное время для созвонов\n'
        f'Выбранное время: {start_time}-{end_time}'
    )
    buttons = [
        [InlineKeyboardButton(timeslot, callback_data=timeslot)]
        for timeslot in TIMESLOTS
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.message.edit_caption(caption, reply_markup=keyboard)

    result = {
        'SET_START_TIME': 'SELECTING_START_HOUR',
        'SET_END_TIME': 'SELECTING_END_HOUR',
    }

    return result[update.callback_query.data]


def set_chosen_start_hour(update: Update, context: CallbackContext):
    context.user_data['start_time'] = update.callback_query.data
    return ask_which_span_part_to_set(update, context)


def set_chosen_end_hour(update: Update, context: CallbackContext):
    context.user_data['end_time'] = update.callback_query.data
    return ask_which_span_part_to_set(update, context)


def go_back(update: Update, context: CallbackContext):
    update.callback_query.answer()

    start_time = context.user_data.get('start_time')
    end_time = context.user_data.get('end_time')
    caption = (
        'Выберите удобное время для созвонов\n'
        f'Выбранное время: {start_time}-{end_time}'
    )
    buttons = [
        [InlineKeyboardButton('Изменить', callback_data='SET_SPAN')],
        [InlineKeyboardButton('Готово', callback_data='CONFIRMATION')],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.message.edit_caption(
        caption,
        reply_markup=keyboard,
    )
    return ConversationHandler.END


def finish_conversation(update: Update, context: CallbackContext):
    update.callback_query.answer()

    chat_id = update.callback_query.from_user.id



    try:
        student = Student.objects.get(chat_id=111)
        star_hour = int(context.user_data['start_time'])
        end_hour = int(context.user_data['end_time'])
        student.start_time = time(hour=star_hour)
        student.end_time = time(hour=end_hour)

        student.save()

        picture = (
            'https://www.freecodecamp.org/news/content/images/size/'
            'w2000/2021/08/chris-ried-ieic5Tq8YMk-unsplash.jpg'
        )
        caption = (
            'Временные возможности приняты.\n'
            'В воскресенье пришлем Вам детали проекта'
        )
    except (Student.DoesNotExist, Student.MultipleObjectsReturned):
        picture = (
            'https://t4.ftcdn.net/jpg/03/08/92/49/'
            '360_F_308924911_jsWAfFOqdSGglzvF7zcNcXIo06eS7Wch.jpg'
        )
        caption = (
            'Что то пошло не так :(\n'
            'Свяжитесь пожалуйста с вашим ментором.'
        )

    update.callback_query.message.reply_photo(
        picture,
        caption,
    )

    return ConversationHandler.END


def main():
    # django.setup()

    tg_bot_token = settings.TG_BOT_TOKEN
    updater = Updater(token=tg_bot_token)
    dispatcher = updater.dispatcher

    time_setting_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                ask_which_span_part_to_set, pattern='^SET_SPAN$'
            )
        ],
        states={
            'SELECTING_WHAT_PART_TO_CHANGE': [
                CallbackQueryHandler(go_back, pattern='^RETURN$'),
                CallbackQueryHandler(select_hour),
            ],
            'SELECTING_START_HOUR': [
                CallbackQueryHandler(set_chosen_start_hour)
            ],
            'SELECTING_END_HOUR': [CallbackQueryHandler(set_chosen_end_hour)],
        },
        fallbacks=[],
        map_to_parent={
            ConversationHandler.END: 'SELECTING_OPTION',
        },
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            'EXPECTING_CONTINUATION': [CallbackQueryHandler(show_time_view)],
            'SELECTING_OPTION': [
                time_setting_handler,
                CallbackQueryHandler(finish_conversation),
            ],
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


class Command(BaseCommand):
    def handle(self, *args, **options):
        main()
