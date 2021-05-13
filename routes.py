from app import app
# from db import db
from services.user_service import user_service

from flask import Flask, render_template, request, url_for, flash, redirect, session
from forms import RegistrationForm, LoginForm
from werkzeug.security import check_password_hash, generate_password_hash


# tietokanta alustetaan nyt psql < schema.sql


restaurants = [{"name": "Skiffer",
                "location": "Helsinki",
                "added_at": "11-5-2021"
                },
               {"name": "Fafa's",
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
                flash(f"The user '{user_exists}' already exists. Please choose another one!",
                      "danger")

            if email_exists is not None:
                flash(f"The email '{email_exists[2]}' is already registered. Please use another one!",
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
