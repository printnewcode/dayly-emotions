import logging
import telebot

from bot.apis.ai import OpenAIAPI
from django.conf import settings

AI_ASSISTANT = OpenAIAPI()

commands = settings.BOT_COMMANDS

bot = telebot.TeleBot(
    settings.BOT_TOKEN,
    threaded=False,
    skip_pending=True,
)

bot.set_my_commands(commands)

logging.info(f'@{bot.get_me().username} started')

logger = telebot.logger
logger.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO, filename="ai_log.log", filemode="w")