from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from movieweb_app import bcrypt, db
from movieweb_app.blueprints.user_auth import SignupForm, SigninForm
from movieweb_app.data_manager.sqltie_data_manager import SQLiteDataManager
from movieweb_app.models import User
from movieweb_app.movie_api_manager.movies_info import MoviesInfo

# Initializing the Blueprint object
users_bp = Blueprint('users', __name__, template_folder='templates', static_folder='static',
                     static_url_path='users_manager/static', url_prefix='/users')


# Initializing the data_db manager object
data_manager = SQLiteDataManager()

def serialize_user_data():
    """
    serializes the data for HTML templating
    :return: user_data: list[dict]
    """
    users_data = []
    users = data_manager.all_users

    for user in users:

        # Gets all the movies of each user. Each movie is a movie object
        user_movies = data_manager.get_user_movies(user.id)

        # Initializing the data_db manager object
        movies_info = MoviesInfo(user_movies)

        serialized_user = {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "likes": user.like_count,
            "date": user.date_registered,
            "favourite_movies": movies_info.total_favourite_movies,
            "highly_rated": movies_info.high_rated_movies,
            "recent_movies": movies_info.recent_movie_release,
            "movies_watched": movies_info.total_movies_watched,
            "worst_rating": movies_info.worst_movie_rating,
            "movie_awards": movies_info.total_movies_with_award,
            "most_movies_countries": movies_info.movies_count_by_countries,
            "top_rated_movie_name": movies_info.top_rated_movie_name,
            "movies": user_movies # movie objects
        }

        users_data.append(serialized_user)
    return users_data


def get_current_user_info(current_user_id):
    """
    Gets the id of the current user and returns a user_data as dictionary
    :param current_user_id: int(logged in user id)
    :return: dict(id:user_id, name: username, ...)
    """
    for user in serialize_user_data():
        if user['id'] == current_user_id:
            return user


@users_bp.route('/', methods=['GET'])
def users_list():
    """
    The route for displaying all users in the 'Users' Tab
    :return: renders the html template users.html
    """
    users = serialize_user_data()
    current_user_info = {}

    # checks if user is signed in.
    # If yes, then remove the data of the signed in user which is to be display it in a separate HTML panel
    if current_user.is_active:
        current_user_info = get_current_user_info(current_user.id)
        users.remove(current_user_info)
    else:
        flash('Sign in to start adding your favorite movies!')

    return render_template('users.html', users=users, signed_in_user=current_user_info)


@users_bp.route('/user_movies/<int:user_id>', methods=['GET'])
@login_required
def user_movies(user_id):
    """
    Route for rending a user's movies' posters in grids
    :param user_id: int
    :return: renders the user_movies.html template
    """
    user = data_manager.get_user_by_id(user_id)
    user_movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, user_movies=user_movies)


@users_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Route to signup user into the app
    :return: renders user_signup.html or redirects users to users.signin
    """
    # If user is already signed in, redirect user to the Users page.
    if current_user.is_authenticated:
        return redirect(url_for('users.users_list'))

    # Handles Post request from the signup form
    form = SignupForm()
    if form.validate_on_submit():
        # Hash the user's password
        password_hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Create a new User instance
        user = User(
            name=form.display_name.data,
            username=form.username.data,
            email=form.email.data,
            password=password_hashed,
            date_registered=datetime.utcnow().strftime('%d-%b-%Y')
        )

        db.session.add(user)
        db.session.commit()

        # Send success message to user and redirect user to signin page
        flash('Your account has been created! You can now sign in.', 'success')
        return redirect(url_for('users.signin'))

    # if GET request, renders the signup form
    return render_template('user_signup.html', form=form)


@users_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    """
    Route that signs in users into the app.
    :return: renders the user_signin.html template
    """
    # If user is already signed in, redirect user to the Users page.
    if current_user.is_authenticated:
        return redirect(url_for('users.users_list'))

    # Handles Post request from the signin form
    form = SigninForm()
    if form.validate_on_submit():
        user = data_manager.get_user_by_email(form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Click the `Account Tab` to add Movies', 'success')

            # redirects user the resource user was trying to access before signin or the users page
            next_page = request.args.get('next')
            return redirect(next_page or url_for('users.users_list'))
        else:
            flash('Error: Please check your email and password', 'error')

    # if GET request, renders the signin form
    return render_template('user_signin.html', form=form)


@users_bp.route('/logout')
def signout():
    """
    signout user from the app
    :return: redirect user to the home page
    """
    logout_user()
    return redirect(url_for('home.home'))


@users_bp.route('/delete_account/<int:user_id>', methods=['POST'])
def delete_account(user_id):
    """
    Route for deleting user account, given a user id
    :param user_id: int
    :return: redirects user to home page
    """
    # Logout the user
    logout_user()

    # Retrieve the user and delete it from the database
    user = data_manager.get_user_by_id(user_id)
    if user:
        # Delete user's associated movies using the  relationship
        db.session.delete(user)
        db.session.commit()
        flash('Your account and associated movies have been deleted.', 'success')
    else:
        flash('Error: User not found!', 'error')
        return redirect(url_for('users.users_list'))

    return redirect(url_for('home.home'))