class User:
    STATE_PAY = 'PAY'
    STATE_SEARCH_IMAGE = 'SEARCH_IMAGE'
    QUESTIONS_STATE = 'question'

    user_id = None
    name = None
    level = None
    roles = []
    page_id = None
    state = None
    question = None
    sub_question = None
    created_at = None
    balance = 100

    def __init__(self, user_id):
        self.user_id = user_id


    def has_question_state(self):
        return self.state == self.QUESTIONS_STATE

    def has_search_image_state(self):
        return self.state == self.STATE_SEARCH_IMAGE

    def has_pay_state(self):
        return self.state == self.STATE_PAY

    def get_data(self):
        return {
            '_id': self.user_id,
            'name': self.name,
            'level': self.level,
            'page_id': self.page_id,
            'state': self.state,
            'created_at': self.created_at,
            'balance': self.balance
        }

    @staticmethod
    def get_user_by_domain(data):
        user = User(data['_id'])

        user.page_id = data['page_id']
        if 'balance' in data:
            user.balance = data['balance']
        if 'state' in data:
            user.state = data['state']

        return user

