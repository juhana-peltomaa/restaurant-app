from app import app
# from db import db
from services.user_service import user_service

from flask import Flask, render_template, request, url_for, flash, redirect, session
from forms import RegistrationForm, LoginForm, ReviewForm
from werkzeug.security import check_password_hash, generate_password_hash


# tietokanta alustetaan nyt psql < schema.sql


restaurants = [{"id": "1",
                "name": "Skiffer",
                "location": "Helsinki",
                "added_at": "11-5-2021"
                },
               {"id": "2",
                "name": "Fafa's",
                "location": "Espoo",
                "added_at": "12-5-2021"
                }
               ]


@app.route('/')
@app.route('/home', methods=['POST', 'GET'])  # both take us to the home page
def home():
    return render_template("home.html", title="Home", posts=restaurants)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":

        if form.validate_on_submit():
            # tarkistetaan onko s.posti tietokannassa
            valid_user = user_service.find_email(form.email.data)

            if valid_user is None:
                flash(f"Email {form.email.data} does not exist!", "danger")
                return render_template("login.html", title="Login", form=form)

            # tarkistetaan onko salasana oikein
            elif check_password_hash(valid_user["password"], form.password.data):

                # luodaan session olio
                session["user"] = valid_user["username"]

                flash(f"Successfully logged in!",
                      "success")
                return render_template("home.html", title="Home Page", posts=restaurants)

            flash(f"Invalid password!", "danger")

        elif not form.validate_on_submit():
            flash(f"Something went wrong login in {form.email.data}!",
                  "danger")

    return render_template("login.html", title="Login", form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if request.method == "POST":
        if form.validate_on_submit():

            username = form.username.data
            password = generate_password_hash(form.password.data)
            email = form.email.data
            admin = form.admin.data

            # checks if user exists, if not registers. Otherwise displays warning
            user_exists = user_service.find_user(username)
            email_exists = user_service.find_email(email)

            if user_exists is not None:
                flash(f"The user '{user_exists.username}' already exists. Please choose another one!",
                      "danger")

            if email_exists is not None:
                flash(f"The email '{email_exists.email}' is already registered. Please use another one!",
                      "danger")

            else:
                # creates new user
                user_service.create_new_user(username, password, email, admin)

                # if validation works, we move to home page
                flash(f"Account {form.username.data} admin status={form.admin.data} successfully created!",
                      "success")

                return redirect(url_for("login"))

            # gives danger message, if anything goes wrong in submitting the regisration
        elif not form.validate_on_submit():
            flash(f"Something went wrong! Enter a valid username and email address!",
                  "danger")

    return render_template("register.html", title="Register", form=form)


@app.route('/logout', methods=["POST"])
def logout():
    try:
        del session["user"]
        flash(f"Successfully logged out and deleted session!",
              "success")
        return redirect("/login")

    except:
        flash(f"Logout not successful, session was not deleted!",
              "warning")
        return redirect("/login")

# Testataan saadaanko ravintolalle oma sivu, johon voidaan lisätä arvostelulomake


@app.route('/review/<int:id>', methods=["GET", "POST"])
def review(id):

    form = ReviewForm()

    reviews = user_service.all_reviews(id)

    try:
        if request.method == "POST":
            if form.validate_on_submit():

                # haetaan käyttäjä, jotta saadaan arvosteluun user_id
                user = user_service.find_user(session["user"])

                content = form.review.data
                stars = form.stars.data
                user_id = user[0]

                # nykyisen ravintolan id
                restaurant_id = id

                if user_service.create_review(content, user_id, restaurant_id):
                    reviews = user_service.all_reviews(id)
                    flash(f"Review was successfully added", "success")
                    return render_template("review.html", id=str(id), posts=restaurants, form=form, reviews=reviews)

        else:
            return render_template("review.html", id=str(id), posts=restaurants, form=form, reviews=reviews)

    except Exception:
        flash(f"Something went wrong adding a review!",
              "danger")
        return render_template("review.html", id=str(id), posts=restaurants, form=form, reviews=reviews)
