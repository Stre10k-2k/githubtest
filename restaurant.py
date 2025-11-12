import telebot
from telebot import types
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

API = os.getenv("APIres")
adminID = os.getenv("adminIDres")
bot = telebot.TeleBot(API)
meal = ""
count = 0

orders = "orders"
ordersFile = os.path.join(orders, "all_orders.txt")
os.makedirs(orders, exist_ok = True)

if not os.path.exists(ordersFile):
    with open(ordersFile, "w", encoding="utf-8")as f:
        f.write("All Orders Logs" + "\n\n")

@bot.message_handler(commands=["start"])
def start(message):
    markUp = types.InlineKeyboardMarkup()
    dish1 = types.InlineKeyboardButton("Burger", callback_data="burger")
    dish2 = types.InlineKeyboardButton("Meat", callback_data="meat")
    dish3 = types.InlineKeyboardButton("Cola", callback_data="cola")
    dish4 = types.InlineKeyboardButton("Salat", callback_data="salat")
    markUp.add(dish1, dish2, dish3, dish4)

    bot.send_message(message.chat.id, "Hello, choose one of dishes", reply_markup=markUp)

@bot.callback_query_handler(func=lambda call: True)
def callCack(call):
    if call.data == "burger":
        bot.send_message(call.message.chat.id, "OK. How many burgers do you want")
    elif call.data == "meat":
        bot.send_message(call.message.chat.id, "OK. How many meat do you want")
    elif call.data == "cola":
        bot.send_message(call.message.chat.id, "OK. How many Coca-Cola do you want")
    elif call.data == "salat":
        bot.send_message(call.message.chat.id, "OK. How many salats do you want")

    meal = call.data

    bot.register_next_step_handler(call.message, lambda message: countOfMeal(message, meal))

def countOfMeal(message, meal):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Please print count, using only nums")
        bot.register_next_step_handler(message, lambda message: countOfMeal(message, meal))
        return
        
    count = message.text.strip()

    orderTime = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")

    bot.send_message(message.chat.id, f"OK. Your order: {count} {meal}")
    bot.send_message(adminID, f"OK. @{message.from_user.username} order: {count} {meal}")

    ordersTXT = (f"{orderTime} \n" f"@{message.from_user.username} order: {count} {meal}\n" "")

    with open(ordersFile, "a", encoding="utf-8") as f:
        f.write(ordersTXT)

bot.infinity_polling()