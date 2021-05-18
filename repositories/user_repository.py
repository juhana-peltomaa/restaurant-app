from db import db
from flask_sqlalchemy import SQLAlchemy


CREATE_NEW_USER = "INSERT INTO users (username, password, email, admin) VALUES (:username, :password, :email, :admin);"

FIND_USER = "SELECT * FROM users WHERE username=:username;"

FIND_EMAIL = "SELECT * FROM users WHERE email=:email;"


class UserRepository:

    def __init__(self, database=db):
        self._db = database

    def create_new_user(self, username, password, email, admin):
        self._db.session.execute(
            CREATE_NEW_USER, {"username": username, "password": password, "email": email, "admin": admin})

        self._db.session.commit()
        return True

    def find_user(self, username):
        result = self._db.session.execute(FIND_USER, {"username": username})

        self._db.session.commit()
        user = result.fetchone()
        return user

    def find_email(self, email):
        result = self._db.session.execute(FIND_EMAIL, {"email": email})

        self._db.session.commit()
        email = result.fetchone()
        return email


user_repository = UserRepository()
