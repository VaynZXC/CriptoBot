# Телеграмм бот - Конвертер криптовалют.
import telebot
from config import keys, TOKEN
from utils import ConversionExeption, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['help', 'start'])
def help(messege: telebot.types.Message):
    text = 'Для того чтобы начать работу введите команду в следующем формате: \n--> имя валюты \ в какую ' \
           'валюту перевести \ количество переводимой валюты. \n \n Увидеть список доступных валют /values'
    bot.reply_to(messege, text)


@bot.message_handler(commands=['values'])
def values(massage: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n -'.join((text, key,))
    bot.reply_to(massage, text)

@bot.message_handler(content_types=['text', ])
def convert(massage: telebot.types.Message):
    try:
        values = massage.text.split(' ')

        if len(values) != 3:
            raise ConversionExeption('Слишком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount) * float(amount)
    except ConversionExeption as e:
        bot.reply_to(massage, f'Ошибка. \n{e}')
    except Exception as e:
        bot.reply_to(massage, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(massage.chat.id, text)


bot.polling(none_stop=True)
