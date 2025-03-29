from datetime import datetime, date

from AI.settings import AI_MODEL
from bot import bot, AI_ASSISTANT
from bot.models import User, DaylyWriting
from bot.texts import START_TEXT

def start(message):
    """Стартовое меню"""
    user = User.objects.filter(user_id=message.chat.id).exists()
    if not user:
        user = User.objects.create(
            user_id = message.chat.id,
            username = message.from_user.username
        )
        user.save()
    bot.send_message(
        text=START_TEXT,
        chat_id=message.chat.id
    )

def new_text(message):
    """Функция для записи мыслей о дне"""
    msg = bot.send_message(
        text="Напишите сюда впечатления или просто свои мысли о сегодняшнем дне !",
        chat_id=message.chat.id
    )
    bot.register_next_step_handler(msg, register_new_text)

def register_new_text(message):
    """Запись мыслей в БД"""
    user = User.objects.get(user_id=message.chat.id)
    dayly_writing = DaylyWriting.objects.filter(day=date.today())

    if not dayly_writing.exists():
        dayly_writing = DaylyWriting.objects.create(user=user, day=date.today())
    else:
        dayly_writing = dayly_writing.first()
    if dayly_writing.writing is None:
        dayly_writing.writing = message.text
    else:
        dayly_writing.writing += f"\n{message.text}"
    dayly_writing.save()
    bot.send_message(
        text="Запись добавлена успешно!",
        chat_id=user.user_id
    )
def get_dayly_writing(message):
    """Получение дневных записей"""
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    msg = bot.send_message(
        text="Для получения записей за определенный день напишите число в формате ГГГГ.М.Д (Пример: 2025.3.20)", 
        chat_id=message.chat.id
        )
    bot.register_next_step_handler(msg, register_get_writing)

def register_get_writing(message):
    """Отправка записей за день"""
    try:
        date_obj = datetime.strptime(message.text, "%Y.%m.%d").date()
    except:
        bot.send_message(text="Ошибка! Попробуйте снова", chat_id=message.chat.id)
        return get_dayly_writing(message)
    user = User.objects.get(user_id=message.chat.id)
    writing = DaylyWriting.objects.filter(user=user, day=date_obj)
    if not writing.exists():
        writing = DaylyWriting.objects.create(user=user, day=date_obj)
    else:
        writing = writing.first()
    if date_obj == date.today():
        if not "Ответ ИИ в этот день" in writing.writing:
            text = f"Вот ваши записи за {date_obj}\n\n"+writing.writing+f"\n\nдень ещё не закончен - напиши свои впечатления!"
        else:
            text = f"Вот ваши записи за {date_obj}\n\n"+writing.writing"
        if writing.writing is None:
            text="День ещё не закончен - напиши свои впечатления!"
    if date_obj < date.today():
        if writing.writing is None:
            text=f"Не смогли найти ваши записи за {date_obj}. Похоже вы не поделились ими в этот день"
        else:
            text=f"Вот ваши записи за {date_obj}\n\n"+writing.writing
    if date_obj > date.today():
        text="Этот день еще не наступил. Но я надеюсь он станет самым лучшим!"
    bot.send_message(
        text=text,
        chat_id=user.user_id
    )
def get_ai_suggestion(text, user, writing):
    """Получение ответа ИИ"""
    response = AI_ASSISTANT.get_response(chat_id=user.user_id, text=text, model=AI_MODEL, max_token=5000)
    response_message = response['message']
    
    bot.send_message(
        text="Вот мнение искуственного интеллекта о вашем дне:\n\n"+f"__{response_message}__",
        chat_id=user.user_id,
        parse_mode="Markdown"
    )
    writing.writing += f"\n\nОтвет ИИ в этот день: {response_message}"
    writing.save()
    
