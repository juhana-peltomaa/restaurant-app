from db import db
from flask_sqlalchemy import SQLAlchemy


CREATE_NEW_REVIEW = "INSERT INTO reviews (title, content, user_id, restaurant_id, sent_at) VALUES (:title, :content, :user_id, :restaurant_id, NOW());"
FIND_REVIEWS = "SELECT * FROM reviews WHERE restaurant_id=:restaurant_id;"


class ReviewRepository:

    def __init__(self, database=db):
        self._db = database

    def create_new_review(self, title, content, user_id, restaurant_id):
        self._db.session.execute(
            CREATE_NEW_REVIEW, {"title": title, "content": content, "user_id": user_id, "restaurant_id": restaurant_id})

        self._db.session.commit()
        return True

    def all_reviews(self, restaurant_id):
        reviews = self._db.session.execute(
            FIND_REVIEWS, {"restaurant_id": restaurant_id})

        rowcount = reviews.rowcount

        self._db.session.commit()

        if rowcount > 0:
            return reviews

        return None


review_repository = ReviewRepository()
