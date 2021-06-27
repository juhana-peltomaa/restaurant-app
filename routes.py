from app import app
# from db import db
from flask import Flask, render_template, request, url_for, flash, redirect, session, abort
from forms import RegistrationForm, LoginForm, ReviewForm, NewRestaurantForm, ReviewFormUpdateMixin, UpdateRestaurantForm
from werkzeug.security import check_password_hash, generate_password_hash
from services.user_service import user_service
from os import urandom


# tietokanta alustetaan nyt psql < schema.sql


@app.route('/')
@app.route('/home')  # both take us to the home page
def home():

    restaurants = user_service.all_rest_and_cat()

    try:
        user_id = session["user_id"]
    except Exception:
        user_id = False

    if restaurants:
        average_reviews = user_service.average_reviews(restaurants)

        if user_id != False:
            favorites = user_service.all_favorites(user_id)

            return render_template("home.html", title="Home", posts=restaurants, reviews=average_reviews, favorites=favorites)

        return render_template("home.html", title="Home", posts=restaurants, reviews=average_reviews, favorites=[])

    return render_template("home.html", title="Home", posts=restaurants, reviews=[], favorites=[])


@app.route('/category/<category>')
def category_show(category):

    restaurants = user_service.rest_and_cat(category)

    try:
        user_id = session["user_id"]
    except Exception:
        user_id = False

    if restaurants:
        average_reviews = user_service.average_reviews(restaurants)

        if user_id != False:
            favorites = user_service.all_favorites(user_id)

            return render_template("category.html", posts=restaurants, reviews=average_reviews, category=category, favorites=favorites)

        return render_template("category.html", posts=restaurants, reviews=average_reviews, category=category, favorites=[])

    flash(f"No restaurants added to the {category.capitalize()} category yet!",
          "warning")
    return redirect("/home")


@app.route('/new', methods=['POST', 'GET'])
def new():
    try:
        if session["admin"] == False:
            flash(f"Access restricted! Only admins can view this page.", "danger")
            return redirect(url_for("home"))
    except KeyError:
        flash(f"Access restricted! Only admins can view this page.", "danger")
        return redirect(url_for("home"))

    form = NewRestaurantForm()

    if request.method == "POST":
        if form.validate_on_submit():

            user = user_service.find_user(session["user"])

            name = form.name.data
            location = form.location.data
            info = form.info.data
            website = form.website.data
            category = form.category.data
            user_id = user[0]

            restaurant_exists = user_service.find_restaurant(name)

            if restaurant_exists is False:

                user_service.add_restaurant(
                    name, location, info, website, user_id, category)
                flash(f"Resturant {name} successfully added!", "success")
                return redirect(url_for("home"))

            else:
                flash(f"Resturant {name} already exists!", "danger")
                return render_template("add_restaurants.html", title="New restaurant", form=form)

    return render_template("add_restaurants.html", title="New restaurant", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":

        if form.validate_on_submit():
            # checks if email is in database and returns user
            valid_user = user_service.find_email(form.email.data)

            if valid_user is None:
                flash(f"Email {form.email.data} does not exist!", "danger")
                return render_template("login.html", title="Login", form=form)

            # checks is password is correct
            elif check_password_hash(valid_user["password"], form.password.data):

                # create session objects to allow showing correct elements
                session["user"] = valid_user["username"]
                session["admin"] = valid_user["admin"]
                session["user_id"] = valid_user["id"]

                flash(f"Successfully logged in!",
                      "success")
                return redirect(url_for('home'))

            flash(f"Invalid password!", "danger")

        elif not form.validate_on_submit():
            flash(f"Something went wrong login in {form.email.data}!",
                  "danger")

    return render_template("login.html", title="Login", form=form)


@ app.route('/register', methods=["GET", "POST"])
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
                flash(f"Account {form.username.data} successfully created!",
                      "success")

                return redirect(url_for("login"))

            # gives danger message, if anything goes wrong in submitting the regisration
        elif not form.validate_on_submit():
            flash(f"Something went wrong! Enter a valid username and email address!",
                  "danger")

    return render_template("register.html", title="Register", form=form)


@ app.route('/logout')
def logout():
    try:
        del session["user"]
        del session["user_id"]
        del session["admin"]

        flash(f"Successfully logged out and deleted session!",
              "success")
        return redirect("/login")

    except:
        flash(f"Logout not successful, session was not deleted!",
              "warning")
        return redirect("/login")


@ app.route('/review/<int:id>', methods=["GET", "POST"])
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
            restaurant_id = id

            review = user_service.create_review(
                title, content, stars, writer, user_id, restaurant_id)

            review = review.first()

            if review is not None:
                reviews = user_service.all_reviews(id)

                flash(
                    f"Review was successfully added!", "success")
                return render_template("review.html", id=id, posts=restaurants, form=form, reviews=reviews)

    return render_template("review.html", id=id, posts=restaurants, form=form, reviews=reviews)


@ app.route('/review/<int:id>/delete/<int:restaurant_id>', methods=["GET", "POST"])
def delete_review(id, restaurant_id):

    delete_review = user_service.delete_review(id, session["user_id"])

    if delete_review:
        flash(f"Review was successfully deleted!", "success")
        return redirect(url_for('review', id=restaurant_id))


@ app.route('/review/<int:id>/edit/<int:restaurant_id>', methods=["GET", "POST"])
def edit(id, restaurant_id):
    form = ReviewFormUpdateMixin()

    review = user_service.find_one_review(id, restaurant_id)
    restaurant = user_service.find_restaurant_id(restaurant_id)

    if request.method == "POST":

        if form.validate_on_submit():

            title = form.title.data
            content = form.review.data
            stars = form.stars.data

            user_service.edit_review(
                title, content, stars, id, restaurant_id)

            flash(f"Review was successfully updated!", "success")
            return redirect(url_for('review', id=restaurant_id))

    return render_template("edit.html", id=id, restaurant_id=restaurant_id, form=form, review=review, restaurant=restaurant)


@ app.route("/delete/<int:restaurant_id>")
def delete(restaurant_id):
    try:
        if session["admin"] == False:
            flash(f"Access restricted! Only admins can view this page.", "danger")
            return redirect(url_for("home"))
    except KeyError:
        flash(f"Access restricted! Only admins can view this page.", "danger")
        return redirect(url_for("home"))

    delete_restaurant = user_service.delete_restaurant(restaurant_id)

    if delete_restaurant is True:
        flash(f"Restaurant successfully deleted!", "success")
        return redirect(url_for('home'))

    flash(f"Deleteing restaurant failed!", "danger")
    return redirect(url_for('home'))


@app.route("/update/<int:restaurant_id>", methods=["GET", "POST"])
def update_restaurant(restaurant_id):

    try:
        if session["admin"] == False:
            flash(f"Access restricted! Only admins can view this page.", "danger")
            return redirect(url_for("home"))
    except KeyError:
        flash(f"Access restricted! Only admins can view this page.", "danger")
        return redirect(url_for("home"))

    form = UpdateRestaurantForm()

    restaurant = user_service.find_restaurant_id(restaurant_id)

    if request.method == "POST":

        if form.validate_on_submit():

            name = form.name.data
            location = form.location.data
            info = form.info.data
            website = form.website.data
            category = form.category.data

            update_restaurant = user_service.update_restaurant(
                name, location, info, website, restaurant_id, category)

            if update_restaurant == True:
                flash(f"Restaurant information was successfully updated!", "success")
                return redirect(url_for('home'))
            else:
                flash(f"Restaurant information was successfully updated!", "success")
                return redirect(url_for('update_restaurant', restaurant_id=restaurant_id))

    return render_template("update.html", id=id, restaurant_id=restaurant_id, form=form, review=review, restaurant=restaurant)


@app.route("/favorite/<int:restaurant_id>")
def favorite_restaurant(restaurant_id):

    restaurant = user_service.find_restaurant_id(restaurant_id)
    user_id = session["user_id"]

    if restaurant:
        favorite = user_service.add_favorite_restaurant(user_id, restaurant_id)

        if favorite == False:
            flash(f"Restaurant is already marked as favorite!", "warning")
            return redirect(request.referrer)

        flash(f"Restaurant marked as favorite!", "success")
        return redirect(request.referrer)


@app.route("/favorite/remove/<int:restaurant_id>")
def remove_favorite(restaurant_id):

    restaurant = user_service.find_restaurant_id(restaurant_id)
    user_id = session["user_id"]

    if restaurant:
        remove = user_service.remove_favorite_restaurant(
            user_id, restaurant_id)

    if remove == False:
        flash(f"Restaurant cannot be removed from favorites!", "warning")
        return redirect(request.referrer)

    flash(f"Restaurant was removed from favorites!", "success")
    return redirect(request.referrer)


@app.route("/profile")
def account():
    try:
        if session["user"] == False:
            flash(f"Access restricted! Login to view your profile.", "danger")
            return redirect(url_for("home"))
    except KeyError:
        flash(f"Access restricted! Login to view your profile.", "danger")
        return redirect(url_for("home"))

    user_info = user_service.find_user(session["user"])

    restaurants = user_service.all_rest_and_cat()

    if user_info:
        try:
            user_id = session["user_id"]
        except Exception:
            user_id = False

        if restaurants:
            average_reviews = user_service.average_reviews(restaurants)

            if user_id != False:
                favorites = user_service.all_favorites(user_id)

            if favorites:
                return render_template("user_profile.html", user=user_info, posts=restaurants, reviews=average_reviews, favorites=favorites)

        return render_template("user_profile.html", user=user_info, posts=[], reviews=[], favorites=[])

    return render_template("user_profile.html", posts=restaurants, reviews=[], favorites=[])
