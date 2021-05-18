import routes
from repositories.review_repository import review_repository as review_repo
from repositories.user_repository import user_repository as user_repo


class UserService:

    def __init__(self, user_repository=user_repo, review_repository=review_repo):
        self._user_repo = user_repository
        self._review_repo = review_repository

    def create_new_user(self, username, password, email, admin):
        self._user_repo.create_new_user(username, password, email, admin)
        return True

    def find_user(self, username):
        exists = self._user_repo.find_user(username)

        if exists:
            return exists
        else:
            return None

    def find_email(self, email):
        email = self._user_repo.find_email(email)

        if email is not None:
            return email
        else:
            return None

    def create_review(self, content, user_id, restaurant_id):

        new_review = self._review_repo.create_new_review(
            content, user_id, restaurant_id)

        if new_review is not None:
            return True

        return False

    def all_reviews(self, id):
        reviews = self._review_repo.all_reviews(id)

        return reviews


user_service = UserService()
