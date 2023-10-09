import datetime
import telebot
from django.shortcuts import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from environs import Env
from telebot import types
from telebot.apihelper import ApiTelegramException
from telebot.types import CallbackQuery
from .models import *
from django.db.models import Q

env = Env()
env.read_env()

# CHANNEL = env.int("CHANNEL")
# ADMIN = env.int("ADMIN")

bot = telebot.TeleBot(env.str("BOT_TOKEN"), parse_mode="HTML")

hideBoard = types.ReplyKeyboardRemove()


@csrf_exempt
def index(request):
    if request.method == "GET":
        return HttpResponse("<a href='http://t.me/dkarimoff96'>Created by</>")
    if request.method == "POST":
        bot.process_new_updates(
            [telebot.types.Update.de_json(request.body.decode("utf-8"))]
        )
        return HttpResponse(status=200)


@bot.message_handler(commands=["start", "send"])
def start(message: types.Message):
    if message.text == "/start":
        user = User.objects.get(user_id=message.from_user.id)
        if not user:
            User.objects.create(
                user_id=message.from_user.id,
                name=message.from_user.first_name,
                active=True,
            )
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        buttons = Type.objects.all()

        buttons_per_row = 2
        markup.add(types.KeyboardButton("Qidiruv"))
        for i in range(0, len(buttons), buttons_per_row):
            row_buttons = buttons[i : i + buttons_per_row]
            markup.row(*[types.KeyboardButton(b.name) for b in row_buttons])
        markup.add(types.KeyboardButton("Ortga"))

        bot.send_message(
            message.from_user.id,
            "Kerakli bo`limni tanlang yoki joy(oshxona, masjid, do`kon..) nomini kiriting!",
            reply_markup=markup,
        )


@bot.message_handler(
    func=lambda message: message.text in [b.name for b in Type.objects.all()]
)
def handle_custom_commands(message: types.Message):
    user = User.objects.get(user_id=message.from_user.id)
    choice = message.text
    user.choice = choice
    user.save()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = City.objects.all()
    buttons_per_row = 2
    for i in range(0, len(buttons), buttons_per_row):
        row_buttons = buttons[i : i + buttons_per_row]
        markup.row(*[types.KeyboardButton(b.name) for b in row_buttons])
    markup.add(types.KeyboardButton("Ortga"))

    bot.send_message(
        message.from_user.id,
        "Shaharni tanlang!",
        reply_markup=markup,
    )


@bot.message_handler(
    func=lambda message: message.text in [b.name for b in City.objects.all()]
)
def handle_custom_commands(message):
    user = User.objects.get(user_id=message.from_user.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    places = Place.objects.filter(city__name=message.text, type__name=user.choice)
    markup.add(types.KeyboardButton("Ortga"))
    if len(places) > 0:
        for place in places:
            text = f"""Joy turi: {place.type}\nJoy nomi: {place.name}\nShahar: {place.city}\nMa'lumot: {place.desc}"""
            bot.send_message(
                message.from_user.id,
                text,
                reply_markup=markup,
            )
    else:
        bot.send_message(
            message.from_user.id,
            "Hudud bo'yicha ma'lumot topilmadi!",
            reply_markup=markup,
        )


@bot.message_handler(func=lambda message: message.text == "Ortga")
def back(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = Type.objects.all()
    buttons_per_row = 2
    markup.add(types.KeyboardButton("Qidiruv"))
    for i in range(0, len(buttons), buttons_per_row):
        row_buttons = buttons[i : i + buttons_per_row]
        markup.row(*[types.KeyboardButton(b.name) for b in row_buttons])

    bot.send_message(
        message.from_user.id,
        "Kerakli bo`limni tanlang !",
        reply_markup=markup,
    )


@bot.message_handler(func=lambda message: message.text == "Qidiruv")
def search(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("Ortga"))
    bot.send_message(
        message.from_user.id,
        "Shahar nomi yoki joy(oshxona, masjid, do`kon..) nomini kiriting",
        reply_markup=markup,
    )
    bot.register_next_step_handler(message, get_search)


def get_search(message: types.Message):
    places = Place.objects.filter(
        Q(name__icontains=message.text) | Q(city__name__icontains=message.text)| Q(type__name__icontains=message.text | Q(desc__icontains=message.text))
    )
    bot.send_message(message.chat.id, f"Hello, {input}. What's your age?")
