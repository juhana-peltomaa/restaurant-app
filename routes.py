from app import app
# from db import db
from flask import Flask, render_template, request, url_for, flash, redirect, session
from forms import RegistrationForm, LoginForm, ReviewForm, NewRestaurantForm, ReviewFormUpdateMixin
from werkzeug.security import check_password_hash, generate_password_hash
from services.user_service import user_service


# tietokanta alustetaan nyt psql < schema.sql

@app.route('/')
@app.route('/home', methods=['POST', 'GET'])  # both take us to the home page
def home():

    restaurants = user_service.find_all_restaurants()

    return render_template("home.html", title="Home", posts=restaurants)


@app.route('/new', methods=['POST', 'GET'])
def new():
    form = NewRestaurantForm()

    if request.method == "POST":
        if form.validate_on_submit():

            user = user_service.find_user(session["user"])

            name = form.name.data
            location = form.location.data
            user_id = user[0]

            restaurant_exists = user_service.find_restaurant(name)

            if restaurant_exists is False:
                user_service.add_restaurant(name, location, user_id)
                flash(f"Resturant {name} successfully added", "success")
                return render_template("add_restaurants.html", title="Add", form=form)

            else:
                flash(f"Resturant {name} already exists", "danger")
                return render_template("add_restaurants.html", title="Add", form=form)

    return render_template("add_restaurants.html", title="Add", form=form)


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

                # haetaan ravintolat - varmaan olemassa järkevämpi tapa toteuttaa
                restaurants = user_service.find_all_restaurants()

                # luodaan session olio
                session["user"] = valid_user["username"]
                session["user_id"] = valid_user["id"]

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
            picture = ""
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
                user_service.create_new_user(
                    username, password, email, picture, admin)

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
        del session["user_id"]
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
    restaurants = user_service.find_all_restaurants()

    if request.method == "POST":
        if form.validate_on_submit():

            title = form.title.data
            content = form.review.data
            stars = form.stars.data
            writer = session["user"]
            user_id = session["user_id"]

            # nykyisen ravintolan id
            restaurant_id = id

            review = user_service.create_review(
                title, content, stars, writer, user_id, restaurant_id)

            review = review.first()

            # Hakee arvostelut, jotta myös uusin näkyy review.html -sivulla
            if review is not None:
                reviews = user_service.all_reviews(id)

                flash(
                    f"Review was successfully added!", "success")
                return render_template("review.html", id=id, posts=restaurants, form=form, reviews=reviews)

    return render_template("review.html", id=id, posts=restaurants, form=form, reviews=reviews)


@app.route('/review/<int:id>/delete/<int:restaurant_id>', methods=["GET", "POST"])
def delete_review(id, restaurant_id):

    delete_review = user_service.delete_review(id, session["user_id"])

    if delete_review:
        flash(f"Review was successfully deleted!", "success")
        return redirect(url_for('review', id=restaurant_id))


@app.route('/review/<int:id>/edit/<int:restaurant_id>', methods=["GET", "POST"])
def edit(id, restaurant_id):
    form = ReviewFormUpdateMixin()

    review = user_service.find_one_review(id, restaurant_id)
    restaurant = user_service.find_restaurant_id(restaurant_id)

    form.title.default = review["title"]
    form.review.default = review["content"]

    if request.method == "POST":

        if form.validate_on_submit():

            title = form.title.data
            content = form.review.data
            stars = form.stars.data

            edit_review = user_service.edit_review(
                title, content, stars, id, restaurant_id)
            print(edit_review)
            print(content)
            print(stars)

            flash(f"Review was successfully updated!", "success")
            return redirect(url_for('review', id=restaurant_id))

    print(form.errors)
    return render_template("edit.html", id=id, restaurant_id=restaurant_id, form=form, review=review, restaurant=restaurant)


# @app.route("/profile")
# def account():
#     image = url_for("static", filename="profile_picture/" + current_user.picture)
#     return render_template("user_profile.html")
