import telebot
from telebot import types
from currency_converter import CurrencyConverter

bot = telebot.TeleBot('6846357616:AAH7MQCH-Qs6I-xSAGWjc8KEkKS9WeKu1Ps')
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Впишите сумму')
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton(text='USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton(text='EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton(text='USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton(text='BRL/EUR', callback_data='brl/eur')
        btn5 = types.InlineKeyboardButton(text='HUF/GBP', callback_data='huf/gbp')
        btn7 = types.InlineKeyboardButton(text='RUB/EUR', callback_data='rub/eur')
        btn8 = types.InlineKeyboardButton(text='Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть > 0. Впишите сумму')
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через слеш')
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(message, summa)
    except Exception as e:
        bot.send_message(message.chat.id, f'Что-то не так: {e}. Впишите значение заново.')
        bot.register_next_step_handler(message, my_currency)

bot.polling(none_stop=True)