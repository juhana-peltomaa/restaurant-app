from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    # validators includes a list of classes responsible for validating inputs
    # DataRequired = makes sure input is not empty
    # Length = takes parameters to ensure certain length of username
    # Email = valid email - Equal = compares 2 inputs
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email",
                        validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
                                     DataRequired(), EqualTo("password")])
    admin = BooleanField("User is admin")

    submit = SubmitField("Create User")


class LoginForm(FlaskForm):
    # validators includes a list of classes responsible for validating inputs
    # DataRequired = makes sure input is not empty
    # Length = takes parameters to ensure certain length of username
    # Email = valid email - Equal = compares 2 inputs
    email = StringField("Email",
                        validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])

    # for cookies
    remember = BooleanField("Remember my login!")

    submit = SubmitField("Login")


class ReviewForm(FlaskForm):
    title = StringField("Title of review", validators=[DataRequired()])
    review = StringField("Your review",
                         validators=[DataRequired()])

    stars = RadioField("Stars", choices=[(
        "1", "☆"), ("2", "☆☆"), ("3", "☆☆☆"), ("4", "☆☆☆☆"), ("5", "☆☆☆☆☆")])

    submit = SubmitField("Add Review")


class NewRestaurantForm(FlaskForm):
    name = StringField("Restaurant name",
                       validators=[DataRequired()])
    location = StringField("Location",
                           validators=[DataRequired()])
    submit = SubmitField("Add new restaurant")
