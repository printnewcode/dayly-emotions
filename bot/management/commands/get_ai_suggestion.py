from datetime import datetime, timedelta, date
from django.core.management.base import BaseCommand, CommandError

from bot.models import User, DaylyWriting
from bot.handlers.common import get_ai_suggestion


class Command(BaseCommand):
    help = "Get suggestion by AI at the end of the day"

    def handle(self, *args, **options):
        dayly_writings = DaylyWriting.objects.filter(day=date.today())
        for writing in dayly_writings:
            if writing is not None:
                if len(writing.writing) > 0:
                    get_ai_suggestion(text=writing.writing, user=writing.user, writing=writing, status=0)