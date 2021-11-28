from django.core.management.base import NoArgsCommand
from tgbot.bot_handler import send_reminder_message


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        send_reminder_message()
