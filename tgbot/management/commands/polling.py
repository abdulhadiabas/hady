from django.core.management.base import NoArgsCommand
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from tgbot.bot_handler import start, handle_voice, handle_text, error, next_question, myscore, help_msg, about, info, \
    send_reminder_msg


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        print("Polling started...")
        # Create the EventHandler and pass it your bot's token.
        updater = Updater("280268931:AAFwB9p4keuIftj0bnwj1fxi6tqeYQiYDsM")

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

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

        # update = Update.de_json(json.loads(request.body.decode("utf-8")), bot)
        # dispatcher.process_update(update)

        # Start the Bot
        updater.start_polling()

        # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()