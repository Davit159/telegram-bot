from telebot.types import InlineKeyboardMarkup
from user import User


class Page:
    message: str
    buttons: InlineKeyboardMarkup
    user: User

    def __init__(self, message: str, buttons: InlineKeyboardMarkup, user: User):
        self.message = message
        self.buttons = buttons
        self.user = user
