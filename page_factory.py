from telebot import types
from page import Page
from user import User
from test_client import Test_Client

class PageFactory:

    client = Test_Client()

    HOME = "home"
    USER = "user"
    SEARCH = "search"
    SEARCH_BY_FOTO = "search_by_foto"
    BALANCE = "balance"
    TOP_UP_BALANCE = "top_up_balance"
    HELP = "help"

    BUTTONS = {
        HOME: types.InlineKeyboardButton("it's home page", callback_data=HOME),
        USER: types.InlineKeyboardButton("🔒Аккаунт", callback_data=USER),
        SEARCH: types.InlineKeyboardButton("🔍Поиск", callback_data=SEARCH),
        SEARCH_BY_FOTO: types.InlineKeyboardButton("📸По Картинке", callback_data=SEARCH_BY_FOTO),
        BALANCE: types.InlineKeyboardButton("💰Баланс", callback_data=BALANCE),
        TOP_UP_BALANCE: types.InlineKeyboardButton("💲Пополнить баланс", callback_data=TOP_UP_BALANCE),
        HELP: types.InlineKeyboardButton("🆘HELP", callback_data=HELP),

    }

    def previous_button(self, previous_page_indicator):
        return types.InlineKeyboardButton("🔙 Назад", callback_data=previous_page_indicator)

    def manage_callback(self, callback):
        BUTTON_TO_CALLBACK = {
            self.HOME: self.home,
            self.USER: self.user,
            self.SEARCH: self.search,
            self.SEARCH_BY_FOTO: self.search_by_foto,
            self.BALANCE: self.balance,
            self.TOP_UP_BALANCE: self.top_up_balance,
            self.HELP: self.help
        }

        callback_indicator = callback.data
        user_indicator = callback.from_user.id
        user = self.client.get_user_by_id(user_indicator)

        # check user exist
        if user is None:
            # registration
            user = self.client.registration(User(user_indicator))

        if callback_indicator in BUTTON_TO_CALLBACK:
            return BUTTON_TO_CALLBACK[callback_indicator](user)

        return self.home(user)

    @staticmethod
    def home(user: User):

        buttons = types.InlineKeyboardMarkup([
            [PageFactory.BUTTONS[PageFactory.SEARCH]],
            [PageFactory.BUTTONS[PageFactory.USER], PageFactory.BUTTONS[PageFactory.TOP_UP_BALANCE]],
        ])

        message = f'''

Это бот c алгоритмом распознавания лиц, который находит профили людей в сец.сетях по фотографиям.

Стоимость одного поиска составляет 1.


Ваш баланс 100
        '''


        return Page(message, buttons, user)



    def user(self, user: User):
        buttons = types.InlineKeyboardMarkup([
            [self.previous_button(self.HOME)]
        ])

        message = f'''
        
Условия пополнения:
К сожилению на данный момент пополнение баланса не доступно.


Ваш баланс - 100
        '''

        return Page(message, buttons, user)

    def search_by_foto(self, user: User):
        buttons = types.InlineKeyboardMarkup([
            [self.previous_button(self.SEARCH)]
        ])
        self.client.update_state(user, User.STATE_SEARCH_IMAGE)

        message = '''
            Для поиска просто загрузите фото.
        '''

        return Page(message, buttons, user)

    def search(self, user: User):
        buttons = types.InlineKeyboardMarkup([
            [self.previous_button(self.HOME)],
            [PageFactory.BUTTONS[PageFactory.SEARCH_BY_FOTO]]
        ])

        message = '''
Доступные соц.сети:
— VK
— Одноклассники

Выберите способ поиска.
        '''

        return Page(message, buttons, user)

    def balance(self, user: User):
        buttons = types.InlineKeyboardMarkup([
            [self.previous_button(self.HOME)],
            [PageFactory.BUTTONS[PageFactory.SEARCH]],
            [PageFactory.BUTTONS[PageFactory.TOP_UP_BALANCE]]
        ])

        message = f'''
        
Условия пополнения

Минимум 10₽
50₽ + 10%
100₽ + 20%
300₽ + 30%

Your balance - {user.balance}₽
'''

        return Page(message, buttons, user)

    def top_up_balance(self, user: User):
        buttons = types.InlineKeyboardMarkup([
            [self.previous_button(self.HOME)]
        ])

        user.state = User.STATE_PAY

        message_1 = f'''
Минимум 10₽
50₽ + 10%
100₽ + 20%
300₽ + 30%

Введите сумму на которую хотите пополнить. 

'''
        message = f'''
        
        К сожилению на данный момент пополнение баланса н доступно.
        
        '''

        return Page(message, buttons, user)

    def balance_error(self, user: User):
        buttons = types.InlineKeyboardMarkup([
            [self.previous_button(self.HOME)]
        ])

        message = f'''
        
        Недостаточный балансю
        
        К сожилению на данный момент пополнение баланса не доступно.
        '''
        return Page(message, buttons, user)

    def help(self, user: User):
        buttons = types.InlineKeyboardMarkup([
            [self.previous_button(self.USER)],
            [PageFactory.BUTTONS[PageFactory.SEARCH]],
            [PageFactory.BUTTONS[PageFactory.TOP_UP_BALANCE]]
        ])

        message = f'''
                1 day - 10₽
                3 day - 25₽
                6 day - 50₽
                20 day - 100₽
                30 day - 140₽
                Limit 10 foto in one day
                Your balance - {user.balance} 
                '''

        return Page(message, buttons, user)