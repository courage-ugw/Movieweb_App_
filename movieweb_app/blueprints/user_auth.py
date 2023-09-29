from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from movieweb_app.data_manager.sqltie_data_manager import SQLiteDataManager


class SignupForm(FlaskForm):
    """
    Signup Form for users
    """
    display_name = StringField('Display Name', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password',
                                                                                             'Confirm password must match password')])
    submit = SubmitField('Sign Up')

    # Initializing Json Data Manager Object
    _data_manager = SQLiteDataManager()

    def validate_username(self, username):
        """
        validates user's username
        :param username:
        :return:
        """

        user = self._data_manager.get_user_by_username(username.data)

        if user:
            raise ValidationError('The username is not available. Please choose another one')

    def validate_email(self, email):
        """
        validates user's email
        :param email:
        :return:
        """

        print(email.data)
        user = self._data_manager.get_user_by_email(email.data)
        print(user)

        if user:
            raise ValidationError('The email already exist!')


class SigninForm(FlaskForm):
    """
    Login Form for users
    """

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')