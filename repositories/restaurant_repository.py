from db import db
from flask_sqlalchemy import SQLAlchemy


CREATE_NEW_RESTAURANT = "INSERT INTO restaurants (name, location, info, website, user_id, added_at) VALUES (:name, :location, :info, :website, :user_id, NOW()) RETURNING id;"

CREATE_NEW_CATEGORY = "INSERT INTO categories (category, category_restaurant_id) VALUES (:category, :category_restaurant_id);"
FIND_RESTAURANT_CATEGORY = "SELECT * FROM categories WHERE category_restaurant_id=:category_restaurant_id;"
FIND_ALL_CATEGORIES = "SELECT * FROM categories;"
FIND_CATEGORY_NAME = "SELECT * FROM categories WHERE category=:category;"

REST_AND_CAT = "SELECT * FROM restaurants JOIN categories ON restaurants.id = categories.category_restaurant_id WHERE categories.category=:category;"
ALL_REST_AND_CAT = "SELECT DISTINCT * FROM restaurants JOIN categories ON restaurants.id = categories.category_restaurant_id;"

FIND_RESTAURANT = "SELECT * FROM restaurants WHERE name=:name;"
FIND_ALL_RESTAURANTS = "SELECT * FROM restaurants;"
FIND_RESTAURANT_ID = "SELECT * FROM restaurants WHERE id=:id;"
DELETE_RESTAURANT = "DELETE FROM restaurants WHERE id=:id;"
UPDATE_RESTAURANT = "UPDATE restaurants SET name=:name, location=:location, info=:info, website=:website WHERE (id=:id) RETURNING id;"

UPDATE_CATEGORY = "UPDATE categories SET category=:category WHERE (category_restaurant_id=:category_restaurant_id) RETURNING id;"

NEW_FAVORITE = "INSERT INTO favorites (favorite_user_id, favorite_restaurant_id) VALUES (:favorite_user_id, :favorite_restaurant_id);"
ALL_FAVORITES = "SELECT * FROM restaurants JOIN favorites ON restaurants.id = favorites.favorite_restaurant_id WHERE favorites.favorite_user_id=:user_id;"
FAVORITE_EXISTS = "SELECT * FROM favorites WHERE favorite_user_id=:favorite_user_id AND favorite_restaurant_id=:favorite_restaurant_id;"
REMOVE_FAVORITES = "DELETE FROM favorites WHERE (favorite_restaurant_id=:favorite_restaurant_id and favorite_user_id=:favorite_user_id) RETURNING id;"


class RestaurantRepository:

    def __init__(self, database=db):
        self._db = database

    def create_new_restaurant(self, name, location, info, website, user_id, category):
        restaurant = self._db.session.execute(
            CREATE_NEW_RESTAURANT, {"name": name, "location": location, "info": info, "website": website, "user_id": user_id})

        restaurant_id = restaurant.fetchone()
        self._db.session.execute(CREATE_NEW_CATEGORY, {
            "category": category, "category_restaurant_id": restaurant_id[0]})

        self._db.session.commit()
        return True

    def find_restaurant(self, name):
        restaurant = self._db.session.execute(
            FIND_RESTAURANT, {"name": name})

        row_count = restaurant.rowcount

        self._db.session.commit()

        if row_count > 0:
            return restaurant

        return False

    def find_all_restaurants(self):
        restaurants = self._db.session.execute(FIND_ALL_RESTAURANTS)

        row_count = restaurants.rowcount

        if row_count > 0:
            return restaurants.fetchall()

        return False

    def find_restaurant_id(self, id):
        restaurant = self._db.session.execute(
            FIND_RESTAURANT_ID, {"id": id})

        row_count = restaurant.rowcount

        self._db.session.commit()

        if row_count > 0:
            return restaurant.fetchone()

        return False

    def delete_restaurant(self, id):
        restaurant = self._db.session.execute(DELETE_RESTAURANT, {"id": id})
        self._db.session.commit()

        # Check if restaurant is still found, return False if exists
        try:
            exists = self.find_restaurant(id)
            return False
        except Exception:
            return True

    def update_restaurant(self, name, location, info, website, id, category=None):
        update_restaurant = self._db.session.execute(UPDATE_RESTAURANT, {
            "name": name, "location": location, "info": info, "website": website, "id": id})

        if category != '':

            category_exists = self.find_category(id)
            # if the restaurant has a category it is updated, otherwise a new one is created
            if category_exists:
                update_category = self._db.session.execute(UPDATE_CATEGORY, {
                    "category": category, "category_restaurant_id": id})
            else:
                self._db.session.execute(CREATE_NEW_CATEGORY, {
                    "category": category, "category_restaurant_id": id})

        self._db.session.commit()
        return True

    def find_category(self, category_restaurant_id):
        category_exists = self._db.session.execute(
            FIND_RESTAURANT_CATEGORY, {'category_restaurant_id': category_restaurant_id})

        row_count = category_exists.rowcount

        self._db.session.commit()

        if row_count > 0:
            print(row_count)
            return True

        return False

    def find_all_categories(self):
        categories = self._db.session.execute(FIND_ALL_CATEGORIES)

        row_count = categories.rowcount

        if row_count > 0:
            return categories.fetchall()

        return False

    def find_category_name(self, category):
        category_set = self._db.session.execute(
            FIND_CATEGORY_NAME, {"category": category})

        row_count = category_set.rowcount

        self._db.session.commit()

        if row_count > 0:
            return category_set.fetchall()

        return False

    def rest_and_cat(self, category):
        category_set = self._db.session.execute(
            REST_AND_CAT, {"category": category})

        row_count = category_set.rowcount

        self._db.session.commit()

        if row_count > 0:
            return category_set.fetchall()

        return False

    def all_rest_and_cat(self):
        category_set = self._db.session.execute(
            ALL_REST_AND_CAT)

        row_count = category_set.rowcount

        self._db.session.commit()

        if row_count > 0:
            return category_set.fetchall()

        return False

    def add_favorite_restaurant(self, favorite_user_id, favorite_restaurant_id):

        check_favorites = self._db.session.execute(
            FAVORITE_EXISTS, {"favorite_user_id": favorite_user_id, "favorite_restaurant_id": favorite_restaurant_id})

        row_count = check_favorites.rowcount

        if row_count > 0:
            return False

        favorite_restaurant = self._db.session.execute(
            NEW_FAVORITE, {"favorite_user_id": favorite_user_id, "favorite_restaurant_id": favorite_restaurant_id})

        self._db.session.commit()

        return True

    def all_favorites(self, user_id):
        favorites = self._db.session.execute(
            ALL_FAVORITES, {"user_id": user_id})

        row_count = favorites.rowcount

        self._db.session.commit()

        if row_count > 0:
            return favorites.fetchall()

        return False

    def remove_favorites(self, favorite_user_id, favorite_restaurant_id):
        remove = self._db.session.execute(REMOVE_FAVORITES, {
                                          "favorite_user_id": favorite_user_id, "favorite_restaurant_id": favorite_restaurant_id})
        self._db.session.commit()

        row_count = remove.rowcount

        if row_count > 0:
            return remove.fetchall()

        return False

    def favorite_exists(self, favorite_user_id):
        favorite_exists = self._db.session.execute(
            FAVORITE_EXISTS, {"favorite_user_id": favorite_user_id})

        row_count = favorite_exists.rowcount

        if row_count > 0:
            return favorite_exists.fetchall()

        self._db.session.commit()

        return False


restaurant_repository = RestaurantRepository()
