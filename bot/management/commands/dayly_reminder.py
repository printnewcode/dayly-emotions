from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError

from bot import bot
from bot.models import User


class Command(BaseCommand):
    help = "Dayly reminder for users"

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            bot.send_message(
                text="Не забудьте записать свои мысли о сегодняшнем дне по команде /new",
                chat_id=user.user_id
            )