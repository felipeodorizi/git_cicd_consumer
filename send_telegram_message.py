import telebot
import sys
import pathlib

bot = telebot.TeleBot("7576015296:AAHPoWA5p6WPrYdcwk_MXXB-EWaN2SBPlLA")
#chat_id = 8552683290
chat_id = -5290134232

def send_message(message):
    """Envia mensagem Telegram"""
    bot.send_message(chat_id, message)

if __name__ == '__main__':
    # sys.argv[0] is the script name itself.
    # sys.argv[1] message

    base = pathlib.Path.cwd()

    if len(sys.argv) > 1:
        message = sys.argv[1]
        send_message(message)
    else:
        print("No Message. Ex: ./send_telegram_message.py 'message'")




