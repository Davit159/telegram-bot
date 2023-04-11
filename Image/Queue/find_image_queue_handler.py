from queue import Queue
from telebot import TeleBot
import time
import threading

import searcher
from page_factory import PageFactory
from test_client import Test_Client
import requests
from searcher import Searcher


class ImageQueueHandler:
    queue: Queue
    bot: TeleBot
    client = Test_Client()
    search = Searcher()

    def __init__(self, bot: TeleBot, queue):
        self.bot = bot
        self.queue = queue

    def start(self):
        thread = threading.Thread(target=self.handle)
        thread.start()
        print('thread started')

    def handle(self):
        while True:
            while not self.queue.empty():
                queue_message = self.queue.get()

                self.bot.edit_message_text(
                    chat_id=queue_message['user_id'],
                    text='поиск начался',
                    message_id=queue_message['our_message_id']
                )

                user = self.client.get_user_by_id(queue_message['user_id'])
                self.client.minus_balance(user)

                raw = queue_message['image_row']
                path = raw + ".jpg"
                file_info = self.bot.get_file(raw)
                file_url = self.bot.get_file_url(file_info.file_id)

                find_data = self.search.search_by_image_url(file_url)
                accounts = find_data["accounts"]
                images = find_data["images"]

                used_account = []
                if len(accounts) > 0:

                    self.bot.delete_message(
                        chat_id=queue_message['user_id'],
                        message_id=queue_message['our_message_id']
                    )
                    for account in accounts:
                        if account["id"] not in used_account:

                            account_url = f"""{self.convert(account)}"""
                            self.bot.send_message(
                                chat_id=queue_message['user_id'],
                                text=account_url
                            )
                            self.bot.send_photo(chat_id=queue_message['user_id'], photo=self.get_image(account, images),
                                                caption="Совпадение.")
                        used_account.append(account["id"])
                else:
                    self.bot.edit_message_text(
                        chat_id=queue_message['user_id'],
                        text='Ничего не найдено.',
                        message_id=queue_message['our_message_id']
                    )



                page = PageFactory.home(user)
                message = self.bot.send_message(chat_id=user.user_id, text=page.message, reply_markup=page.buttons)
                self.client.update_page_id(user, message.id)

                print('We have a message.')

            time.sleep(2)

    def convert(self, account):
        if account["provider"] == "OK":
            return f"https://ok.ru/profile/{account['id']}"
        elif account["provider"] == "VK":
            return f"https://vk.ru/{account['id']}"
        return ""

    def send_image(self):
        pass

    def get_image(self, account_data, images):
        print(account_data)
        print(images)
        for image in images:
            if image in account_data["images"]:
                return account_data["images"][image]

        return None
