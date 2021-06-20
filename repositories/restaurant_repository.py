from db import db
from flask_sqlalchemy import SQLAlchemy


CREATE_NEW_RESTAURANT = "INSERT INTO restaurants (name, location, info, website, user_id, added_at) VALUES (:name, :location, :info, :website, :user_id, NOW()) RETURNING id;"

CREATE_NEW_CATEGORY = "INSERT INTO categories (category, restaurant_id) VALUES (:category, :restaurant_id);"
FIND_RESTAURANT_CATEGORY = "SELECT * FROM categories WHERE restaurant_id=:restaurant_id;"
FIND_ALL_CATEGORIES = "SELECT * FROM categories;"
FIND_CATEGORY_NAME = "SELECT * FROM categories WHERE category=:category;"

REST_AND_CAT = "SELECT * FROM restaurants JOIN categories ON restaurants.id = categories.restaurant_id WHERE categories.category=:category;"
ALL_REST_AND_CAT = "SELECT * FROM restaurants JOIN categories ON restaurants.id = categories.restaurant_id;"

FIND_RESTAURANT = "SELECT * FROM restaurants WHERE name=:name;"
FIND_ALL_RESTAURANTS = "SELECT * FROM restaurants;"
FIND_RESTAURANT_ID = "SELECT * FROM restaurants WHERE id=:id;"
DELETE_RESTAURANT = "DELETE FROM restaurants WHERE id=:id;"
UPDATE_RESTAURANT = "UPDATE restaurants SET name=:name, location=:location, info=:info, website=:website WHERE (id=:id) RETURNING id;"

UPDATE_CATEGORY = "UPDATE categories SET category=:category WHERE (restaurant_id=:restaurant_id) RETURNING id;"


class RestaurantRepository:

    def __init__(self, database=db):
        self._db = database

    def create_new_restaurant(self, name, location, info, website, user_id, category):
        restaurant = self._db.session.execute(
            CREATE_NEW_RESTAURANT, {"name": name, "location": location, "info": info, "website": website, "user_id": user_id})

        print("Category:", category)
        print("type", type(category))

        restaurant_id = restaurant.fetchone()
        self._db.session.execute(CREATE_NEW_CATEGORY, {
            "category": category, "restaurant_id": restaurant_id[0]})

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
                    "category": category, "restaurant_id": id})
            else:
                self._db.session.execute(CREATE_NEW_CATEGORY, {
                    "category": category, "restaurant_id": id})

        self._db.session.commit()
        return True

    def find_category(self, restaurant_id):
        category_exists = self._db.session.execute(
            FIND_RESTAURANT_CATEGORY, {'restaurant_id': restaurant_id})

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


restaurant_repository = RestaurantRepository()
