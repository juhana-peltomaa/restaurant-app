import routes
from repositories.user_repository import user_repository as user_repo


class UserService:

    def __init__(self, user_repository=user_repo):
        self._user_repo = user_repository

    def create_new_user(self, username, password, email, admin):
        self._user_repo.create_new_user(username, password, email, admin)
        return True

    def find_user(self, username):
        if self._user_repo.find_user(username):
            return username
        else:
            return None

    def find_email(self, email):
        email = self._user_repo.find_email(email)

        if email is not None:
            return email
        else:
            return None


user_service = UserService()
