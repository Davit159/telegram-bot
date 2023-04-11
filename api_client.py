from abc import ABC, abstractmethod
from user import User


class ApiInterface:

    @abstractmethod
    def get_user_by_id(self, user_id):
        pass

    @abstractmethod
    def registration(self, user: User):
        pass

    @abstractmethod
    def update_page_id(self, user_id, page_id):
        pass

    @abstractmethod
    def get_question_by_id(self, question_id):
        pass

    @abstractmethod
    def next_sub_question(self, user: User):
        pass

    @abstractmethod
    def attach_question(self, user: User):
        pass
