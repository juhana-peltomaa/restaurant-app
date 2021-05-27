from db import db
from flask_sqlalchemy import SQLAlchemy


CREATE_NEW_REVIEW = "INSERT INTO reviews (title, content, stars, writer, user_id, restaurant_id, sent_at) VALUES (:title, :content, :stars, :writer, :user_id, :restaurant_id, NOW()) RETURNING id, user_id;"
FIND_REVIEWS = "SELECT * FROM reviews WHERE restaurant_id=:restaurant_id;"
FIND_REVIEW_WRITER = "SELECT u.username FROM users u INNER JOIN reviews r ON (r.user_id=:user_id) WHERE r.id=:review_id;"
DELETE_REVIEW = "DELETE FROM reviews WHERE id=:id AND user_id=:user_id;"


class ReviewRepository:

    def __init__(self, database=db):
        self._db = database

    def create_new_review(self, title, content, stars, writer, user_id, restaurant_id):
        new_review = self._db.session.execute(
            CREATE_NEW_REVIEW, {"title": title, "content": content, "stars": stars, "writer": writer, "user_id": user_id, "restaurant_id": restaurant_id})

        self._db.session.commit()

        rowcount = new_review.rowcount

        if rowcount > 0:
            # Palauttaa RETURNING komennon kautta id:n ja user_id:n
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

    def find_review_writer(self, review_id, user_id):
        review_writer = self._db.session.execute(FIND_REVIEW_WRITER, {
            "review_id": review_id, "user_id": user_id})

        self._db.session.commit()

        # DRY ongelmaa tässä, mieti järkevämpi tapa tsekata, että SQL komennot menee läpi
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


review_repository = ReviewRepository()
