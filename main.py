import os
import telebot
from page_factory import PageFactory
import json
from queue import Queue
from test_client import Test_Client
from message_handler import MessageHandler
from Image.Queue.find_image_queue_handler import ImageQueueHandler
import time

from user import User

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
page_factory = PageFactory()
client = Test_Client()
handler_message = MessageHandler()
image_queue = Queue()
image_queue_handler = ImageQueueHandler(bot, image_queue)
image_queue_handler.start()


@bot.message_handler(commands=['start'])
def start(message):
    global client
    user_id = message.chat.id
    user = client.get_user_by_id(user_id)

    if user is None:
        # registration
        user = client.registration(User(user_id))

    page = PageFactory.home(user_id)

    message = bot.send_message(chat_id=user_id, text=page.message, reply_markup=page.buttons)

    client.update_page_id(user, message.id)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global client
    page = page_factory.manage_callback(call)
    user = page.user

    if user.page_id is not None:
        bot.edit_message_text(chat_id=call.from_user.id, message_id=user.page_id, text=page.message, reply_markup=page.buttons)
    else:
        message = bot.send_message(chat_id=call.from_user.id, text=page.message, reply_markup=page.buttons)
        client.update_page_id(user, message.id)


# @bot.message_handler(func=lambda m: True)
# def message_handler(message):
#     global client
#     global handler_message
#     print(message)
#     user = client.get_user_by_id(message.from_user.id)
#     if user is None:
#         # registration
#         user = client.registration(message.from_user.id)
#     bot.reply_to(message, handler_message.handle(message, user))


@bot.message_handler(func=lambda m: True, content_types=['photo'])
def photo_message_handler(message):
    global client
    global handler_message
    global image_queue

    user = client.get_user_by_id(message.from_user.id)
    if user is not None:
        # no registration
        raw = message.photo[-1].file_id
        if user.balance > 0:
            our_message = bot.reply_to(message, handler_message.handle(message, user))
            image_queue.put({'image_row': raw, 'user_id': user.user_id, 'our_message_id': our_message.message_id})
        else:
            page = page_factory.balance_error(user)

            message = bot.send_message(chat_id=user.user_id, text=page.message, reply_markup=page.buttons)
            client.update_page_id(user, message.id)


bot.polling()
