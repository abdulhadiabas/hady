import json
import logging
from queue import Queue
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.bot import Bot
from telegram.ext import CommandHandler, MessageHandler, \
    CallbackQueryHandler, Filters, Dispatcher, InlineQueryHandler

from tgbot.bot_handler import start, handle_voice, handle_text, error, next_question, myscore, info, help_msg, about, \
    send_reminder_msg

from telegram.ext import Updater, CommandHandler

from telegram.ext import Updater, CommandHandler

updater = Updater(token="2103492201:AAFBZ-7JCPjKROtuLlsnslgfwaSAiow4kE8")
dispatcher = updater.dispatcher


start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)
updater.start_polling()

start_handler = CommandHandler("next", next_question)
dispatcher.add_handler(start_handler)
updater.start_polling()

start_handler = CommandHandler("myscore", myscore)
dispatcher.add_handler(start_handler)
updater.start_polling()

start_handler = CommandHandler("handle_text", handle_text)
dispatcher.add_handler(start_handler)
updater.start_polling()

start_handler = CommandHandler("help", help_msg)
dispatcher.add_handler(start_handler)
updater.start_polling()

start_handler = CommandHandler("info", info)
dispatcher.add_handler(start_handler)
updater.start_polling()

start_handler = CommandHandler("reminder", send_reminder_msg)
dispatcher.add_handler(start_handler)
updater.start_polling()

start_handler = CommandHandler("home", start)
dispatcher.add_handler(start_handler)
updater.start_polling()

start_handler = MessageHandler(Filters.voice, handle_voice)
dispatcher.add_handler(start_handler)
updater.start_polling()

start_handler = MessageHandler(Filters.text, handle_text)
dispatcher.add_handler(start_handler)
updater.start_polling()
@csrf_exempt
def webhook(request):
    bot = Bot("2103492201:AAFBZ-7JCPjKROtuLlsnslgfwaSAiow4kE8")

    dispatcher = updater.dispatcher
    # The command
    # dispatcher.add_handler(InlineQueryHandler(inlinequery_handler))
    # dispatcher.add_handler(CallbackQueryHandler(callback_handler))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('next', next_question))
    dispatcher.add_handler(CommandHandler('myscore', myscore))
    dispatcher.add_handler(CommandHandler('help', help_msg))
    dispatcher.add_handler(CommandHandler('about', about))
    dispatcher.add_handler(CommandHandler('info', info))
    dispatcher.add_handler(CommandHandler('reminder', send_reminder_msg))
    dispatcher.add_handler(CommandHandler('home', start))
    dispatcher.add_handler(MessageHandler(Filters.voice, handle_voice))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_text))
    dispatcher.add_error_handler(error)

    update = Update.de_json(json.loads(request.body.decode("utf-8")), bot)

    dispatcher.process_update(update)

    return HttpResponse(status=200)
