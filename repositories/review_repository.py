from db import db
from flask_sqlalchemy import SQLAlchemy


CREATE_NEW_REVIEW = "INSERT INTO reviews (title, content, stars, writer, user_id, restaurant_id, sent_at) VALUES (:title, :content, :stars, :writer, :user_id, :restaurant_id, NOW()) RETURNING id, user_id;"
FIND_REVIEWS = "SELECT * FROM reviews WHERE restaurant_id=:restaurant_id;"
FIND_REVIEW_WRITER = "SELECT u.username FROM users u INNER JOIN reviews r ON (r.user_id=:user_id) WHERE r.id=:review_id;"
DELETE_REVIEW = "DELETE FROM reviews WHERE id=:id AND user_id=:user_id;"
FIND_ONE_REVIEW = "SELECT * FROM reviews WHERE id=:id AND restaurant_id=:restaurant_id;"
UPDATE_REVIEW = "UPDATE reviews SET title=:title, content=:content, stars=:stars WHERE (id=:id AND restaurant_id=:restaurant_id);"

AVERAGE_REVIEW = "SELECT ROUND(AVG(stars)::numeric, 1) FROM reviews WHERE restaurant_id=:restaurant_id;"


class ReviewRepository:

    def __init__(self, database=db):
        self._db = database

    def create_new_review(self, title, content, stars, writer, user_id, restaurant_id):
        new_review = self._db.session.execute(
            CREATE_NEW_REVIEW, {"title": title, "content": content, "stars": stars, "writer": writer, "user_id": user_id, "restaurant_id": restaurant_id})

        self._db.session.commit()

        rowcount = new_review.rowcount

        if rowcount > 0:
            return new_review

        return None

    def all_reviews(self, restaurant_id):
        reviews = self._db.session.execute(
            FIND_REVIEWS, {"restaurant_id": restaurant_id})

        rowcount = reviews.rowcount

        self._db.session.commit()

        if rowcount > 0:
            return reviews

        return None

    def find_one_review(self, id, restaurant_id):
        review = self._db.session.execute(
            FIND_ONE_REVIEW, {"id": id, "restaurant_id": restaurant_id})

        rowcount = review.rowcount

        self._db.session.commit()

        if rowcount > 0:
            return review.fetchone()

        return None

    def find_review_writer(self, review_id, user_id):
        review_writer = self._db.session.execute(FIND_REVIEW_WRITER, {
            "review_id": review_id, "user_id": user_id})

        self._db.session.commit()

        rowcount = review_writer.rowcount

        self._db.session.commit()

        if rowcount > 0:
            row = review_writer.fetchone()
            return row

        return None

    def delete_review(self, id, user_id):
        delete_review = self._db.session.execute(
            DELETE_REVIEW, {"id": id, "user_id": user_id})

        rowcount = delete_review.rowcount

        self._db.session.commit()

        if rowcount > 0:
            return True

        return False

    def edit_review(self, title, content, stars, id, restaurant_id):
        self._db.session.execute(UPDATE_REVIEW, {
            "title": title, "content": content, "stars": stars, "id": id, "restaurant_id": restaurant_id})
        self._db.session.commit()

        return True

    def average_reviews(self, restaurant_id):

        try:
            average_review = self._db.session.execute(
                AVERAGE_REVIEW, {"restaurant_id": restaurant_id})
            self._db.session.commit()

        except Exception:
            return "Something went wrong"

        return average_review.fetchone()


review_repository = ReviewRepository()
