from user import User


class MessageHandler:

    def handle(self, message, user: User):
        if user.has_pay_state():
            return self.handle_pay_message(message, user)
        elif user.has_search_image_state():
            return self.handle_image_search_message(message, user)
        return "I don't know what do you want"

    def handle_pay_message(self, message, user: User):
        if message.content_type == 'text' and user is not None:
            print(message)
            print('bef error')
            text = message.text
            try:
                if int(text) > 9.999:
                    if user.state == User.STATE_PAY:
                        user.page_id = None
                        return 'hear will be pay link'
                return ('some error')
            except:
                return 'Some misstace handling pay message'

    def handle_image_message(self, message, user: User):
        if message.content_type == 'text' and user is not None:
            text = message.text
            try:
                if int(text) > 9.999:
                    if user.state == 'balance':
                        user.page_id = None
                        return 'hear will be pay link'
            except:
                return 'Some misstace handling pay message'

    def handle_image_search_message(self, message, user: User):
        print(message)
        return 'Ваш запрос добавлен в очередь.'
