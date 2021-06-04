from db import db
from flask_sqlalchemy import SQLAlchemy


CREATE_NEW_RESTAURANT = "INSERT INTO restaurants (name, location, user_id, added_at) VALUES (:name, :location, :user_id, NOW());"
FIND_RESTAURANT = "SELECT * FROM restaurants WHERE name=:name;"
FIND_ALL_RESTAURANTS = "SELECT * FROM restaurants;"
FIND_RESTAURANT_ID = "SELECT * FROM restaurants WHERE id=:id;"
DELETE_RESTAURANT = "DELETE FROM restaurants WHERE id=:id;"


class RestaurantRepository:

    def __init__(self, database=db):
        self._db = database

    def create_new_restaurant(self, name, location, user_id):
        self._db.session.execute(
            CREATE_NEW_RESTAURANT, {"name": name, "location": location, "user_id": user_id})

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
            return restaurants

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


restaurant_repository = RestaurantRepository()
