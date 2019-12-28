import telegram.ext
from telegram.ext import Updater, CommandHandler
import logging
from change import get_exchange_rate_eur, get_exchange_rate_usd
from datetime import datetime

updater = Updater(token='1053815885:AAH4s7Y034k8UoqOm7N-vJqF8uTwqkdQJKo', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hey there! Use commands /usd and /eur to get\n'
                                                                    'an exchange rate of dollar and euro compare to ruble\n'
                                                                    'To get every day notifications use /time HH:MM')


def dollar(update, context):
    message = get_exchange_rate_usd()
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def euro(update, context):
    message = get_exchange_rate_eur()
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def notification(context: telegram.ext.CallbackContext):
    message1 = 'usd: ' + str(get_exchange_rate_usd())
    message2 = 'eur: ' + str(get_exchange_rate_eur())

    context.bot.send_message(chat_id=context.job.context, text=message1)
    context.bot.send_message(chat_id=context.job.context, text=message2)


def notification_time(update: telegram.Update, context: telegram.ext.CallbackContext):
    try:
        string_time = datetime.strptime(context.args[0], '%H:%M')
        time = string_time.time()

        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Sure! I\'m going to send you notification at {} every day!'.format(context.args[0]))
        context.job_queue.run_daily(notification, time=time, context=update.message.chat_id)

    except ValueError:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text= 'Your time is not correct. Use HH:MM format')
        return


def main():
    euro_handler = CommandHandler('eur', euro)
    dispatcher.add_handler(euro_handler)

    dollar_handler = CommandHandler('usd', dollar)
    dispatcher.add_handler(dollar_handler)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    timer_handler = CommandHandler('time', notification_time)
    updater.dispatcher.add_handler(timer_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
