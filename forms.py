from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, SelectField
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
    title = StringField("Review Title", validators=[DataRequired()])
    review = StringField("Your review",
                         validators=[DataRequired()])

    stars = RadioField("Rating", choices=[(
        "1", "☆"), ("2", "☆☆"), ("3", "☆☆☆"), ("4", "☆☆☆☆"), ("5", "☆☆☆☆☆")])

    submit = SubmitField("Add Review")


class ReviewFormUpdateMixin(FlaskForm):
    title = StringField("New review title", validators=[DataRequired()])
    review = StringField("New review",
                         validators=[DataRequired()])

    stars = RadioField("New rating", choices=[(
        "1", "☆"), ("2", "☆☆"), ("3", "☆☆☆"), ("4", "☆☆☆☆"), ("5", "☆☆☆☆☆")])

    submit = SubmitField("Confirm review edits")


class NewRestaurantForm(FlaskForm):
    name = StringField("Restaurant name",
                       validators=[DataRequired()])
    location = StringField("Location",
                           validators=[DataRequired()])
    info = StringField("Info",
                       validators=[DataRequired()])
    website = StringField("Website")
    category = SelectField(u"Category", choices=["",
                                                 'Breakfest', 'Brunch', 'Cafe', 'Lunch', 'Dinner'])
    submit = SubmitField("Add new restaurant")


class UpdateRestaurantForm(FlaskForm):
    name = StringField("Update restaurant name",
                       validators=[DataRequired()])
    location = StringField("Update location",
                           validators=[DataRequired()])
    info = StringField("Update info",
                       validators=[DataRequired()])
    website = StringField("Update website")
    category = SelectField(u"Category", choices=["",
                                                 'Breakfest', 'Brunch', 'Cafe', 'Lunch', 'Dinner'])
    submit = SubmitField("Confirm updates")
