import telebot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()
adminID = os.getenv("adminID")

bot = telebot.TeleBot(os.getenv("API_KEY"))
tasks = []

@bot.message_handler(func=lambda m: m.chat.id != adminID)
def forward(message):
    bot.forward_message(adminID, message.chat.id, message.message_id)

@bot.message_handler(func=lambda m: m.chat.id == adminID and m.reply_to_message)
def answer(message):
    if message.reply_to_message:
        userID = message.reply_to_message.forward_from.id
        bot.send_message(userID, f"Admin said: {message.text}")

@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    addBtn = types.KeyboardButton("/add")
    listBtn = types.KeyboardButton("/list")
    photoBtn = types.KeyboardButton("/noteph")
    keyboard.add(addBtn, listBtn, photoBtn)

    bot.send_message(message.chat.id, "Hello, here you can write your To-Do List!", reply_markup=keyboard)

@bot.message_handler(commands=["add"])
def add(message):
    if message.text[4:].strip() == "":
        bot.send_message(message.chat.id, "Please write your task actually after '/add'")

        return
    
    markUp = types.InlineKeyboardMarkup()
    btnList = types.InlineKeyboardButton("List", callback_data="/list")
    btnPhoto = types.InlineKeyboardButton("Photo", callback_data="/noteph")
    markUp.add(btnList, btnPhoto)

    bot.send_message(message.chat.id, f"Your task ' {message.text[4:].strip().capitalize()} ', added", reply_markup=markUp)
    tasks.append(message.text[4:].strip().capitalize())

@bot.callback_query_handler(func=lambda call: True)
def callBack(call):
    if call.data == "/list":
        for i in tasks:
            bot.send_message(call.message.chat.id, i)
    elif call.data == "/noteph":
        url = "https://i.pinimg.com/originals/3a/f0/8f/3af08f377b368305e6d054ab49231d10.jpg"
        bot.send_photo(call.message.chat.id, url, caption="It's your notepad")
    
@bot.message_handler(commands=["list"])
def list(message):
    if tasks == []:
        bot.send_message(message.chat.id, "You dont have any tasks")

        return

    for i in tasks:
        bot.send_message(message.chat.id, i)

@bot.message_handler(content_types=["photo"])
def photo(message):
    bot.send_message(message.chat.id, "Nice photo dear! But I hope you send me text!")

@bot.message_handler(content_types=["document"])
def photo(message):
    bot.send_message(message.chat.id, "Nice document buisnessman! But I hope you send me text!")

@bot.message_handler(content_types=["sticker"])
def photo(message):
    bot.send_message(message.chat.id, "Nice sticker bro! But I hope you send me text!")

@bot.message_handler(commands=["noteph"])
def sendPhoto(message):
    url = "https://i.pinimg.com/originals/3a/f0/8f/3af08f377b368305e6d054ab49231d10.jpg"
    bot.send_photo(message.chat.id, url, caption="It's your notepad")
    
bot.infinity_polling()