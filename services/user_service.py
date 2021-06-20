import routes
from repositories.review_repository import review_repository as review_repo
from repositories.user_repository import user_repository as user_repo
from repositories.restaurant_repository import restaurant_repository as rest_repo


class UserService:

    def __init__(self, user_repository=user_repo, review_repository=review_repo, restaurant_repository=rest_repo):
        self._user_repo = user_repository
        self._review_repo = review_repository
        self._rest_repo = rest_repo

    def create_new_user(self, username, password, email, picture, admin):
        self._user_repo.create_new_user(
            username, password, email, picture, admin)
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

    def create_review(self, title, content, stars, writer, user_id, restaurant_id):

        new_review = self._review_repo.create_new_review(
            title, content, stars, writer, user_id, restaurant_id)

        if new_review is not None:
            return new_review

        return None

    def review_writer(self, review_id, user_id):
        review_writer = self._review_repo.find_review_writer(
            review_id, user_id)

        return review_writer

    def all_reviews(self, id):
        reviews = self._review_repo.all_reviews(id)

        return reviews

    def find_restaurant(self, name):
        restaurant = self._rest_repo.find_restaurant(name)

        return restaurant

    def add_restaurant(self, name, location, info, website, user_id, category):

        new_resturant = self._rest_repo.create_new_restaurant(
            name, location, info, website, user_id, category)

        if new_resturant is not None:
            return True

        return False

    def find_all_restaurants(self):
        restaurants = self._rest_repo.find_all_restaurants()

        return restaurants

    def delete_review(self, review_id, user_id):
        return self._review_repo.delete_review(review_id, user_id)

    def find_restaurant_id(self, id):
        restaurant = self._rest_repo.find_restaurant_id(id)

        return restaurant

    def find_one_review(self, review_id, restaurant_id):
        return self._review_repo.find_one_review(review_id, restaurant_id)

    def edit_review(self, title, content, stars, id, restaurant_id):
        return self._review_repo.edit_review(title, content, stars, id, restaurant_id)

    def delete_restaurant(self, restaurant_id):
        return self._rest_repo.delete_restaurant(restaurant_id)

    def average_reviews(self, restaurants):

        average_reviews = []

        for restaurant in restaurants:

            review = self._review_repo.average_reviews(
                restaurant[0])

            if review[0] == None:
                average_reviews.append(None)

            else:
                average_reviews.append(float(review[0]))

        return average_reviews

    def update_restaurant(self, name, location, info, website, restaurant_id, category):
        return self._rest_repo.update_restaurant(name, location, info, website, restaurant_id, category)

    def find_all_categories(self):
        categories = self._rest_repo.find_all_categories()
        return categories

    def find_category_name(self, category):
        category_set = self._rest_repo.find_category_name(category)

        return category_set

    def rest_and_cat(self, category):
        category_set = self._rest_repo.rest_and_cat(category.capitalize())

        return category_set

    def all_rest_and_cat(self):
        category_set = self._rest_repo.all_rest_and_cat()

        return category_set


user_service = UserService()
