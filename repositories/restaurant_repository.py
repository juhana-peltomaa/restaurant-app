from db import db
from flask_sqlalchemy import SQLAlchemy


CREATE_NEW_RESTAURANT = "INSERT INTO restaurants (name, location, user_id, added_at) VALUES (:name, :location, :user_id, NOW());"
FIND_RESTAURANT = "SELECT * FROM restaurants WHERE name=:name;"
FIND_ALL_RESTAURANTS = "SELECT * FROM restaurants;"


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

        rowcount = restaurant.rowcount

        self._db.session.commit()

        if rowcount > 0:
            return restaurant

        return False

    def find_all_restaurants(self):
        restaurants = self._db.session.execute(FIND_ALL_RESTAURANTS)

        rowcount = restaurants.rowcount

        if rowcount > 0:
            return restaurants

        return False


restaurant_repository = RestaurantRepository()
