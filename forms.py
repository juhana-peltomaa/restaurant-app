from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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
