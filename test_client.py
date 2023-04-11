from api_client import ApiInterface
from user import User
import pymongo


class Test_Client(ApiInterface):

    client = pymongo.MongoClient('mongodb+srv://davo:davo1@cluster0.5walz.mongodb.net/myFirstDatabase?retryWrites'
                                 '=true&w=majority')

    table = client['staging_teacher']

    users = table["user"]

    def get_user_by_id(self, user_id) -> User or None:

        user = self.table['user'].find_one({'_id': user_id})
        if user is not None:
            return User.get_user_by_domain(user)

        return None

    def registration(self, user: User) -> User:

        self.table['user'].insert_one(user.get_data())
        return user

    def update_last_page(self, user_id, page_id):
        if user_id in self.users:
            self.users[user_id].previous_page = page_id

    def update_page_id(self, user, page_id):
        self.table['user'].update_one({'_id': user.user_id}, {'$set': {"page_id": page_id}})

    def get_question_by_id(self, question_id):
        return self.table['question'].find_one({'_id': question_id})

    def next_sub_question(self, user: User):
        self.table['user'].update_one({'_id': user.user_id}, {'$set': {"sub_question": user.sub_question + 1}})
        user.sub_question += 1

    def attach_question(self, user: User):
        question = self.table['question'].find_one()
        self.table['user'].update_one(
            {'_id': user.user_id},
            {'$set':{"sub_question": 0, "question": question['_id'], "state": User.QUESTIONS_STATE}})
        return question

    def update_state(self, user, state):
        self.users.update_one({'_id': user.user_id}, {'$set': {"state": state}})
        user.state = state

    def minus_balance(self, user):
        user.balance -= 1
        self.users.update_one({'_id': user.user_id}, {'$set': {"balance": user.balance}})

    # def registration(self, user_id) -> User:
    #     user = User(user_id)
    #     self.users[user_id] = user
    #     return user
    #
    # def update_last_page(self, user_id, page_id):
    #     if user_id in self.users:
    #         self.users[user_id].previous_page = page_id
    #
    # def update_page_id(self, user_id, page_id):
    #     user = self.get_user_by_id(user_id)
    #     if user is not None:
    #         user.page_id = page_id
