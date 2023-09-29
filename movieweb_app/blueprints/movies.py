from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from movieweb_app import db
from movieweb_app.data_manager.sqltie_data_manager import SQLiteDataManager
from movieweb_app.models import UserMovie, Movie
from movieweb_app.movie_api_manager.movie_data_fetcher import MovieDataFetcher

# Movies Blueprint
movies_bp = Blueprint('movies', __name__, template_folder='templates', static_folder='static',
                      static_url_path='users_manager/static', url_prefix='/users/account/')

# Creating a data_db manager object
data_manager = SQLiteDataManager()

# Creates instance the movie data_db fetcher object that fetches movies data_db from IMDb movies api
movies_data = MovieDataFetcher()

def new_movie_id():
    """
    Generates a new id for new movie object. Returns the value of the id as int.
    :return: int
    """
    return max([movie.id for movie in data_manager.all_movies]) + 1

def get_movies_data(movie_name):
    """
    Gets a movie name as parameter and returns a movie object
    :param movie_name: string
    :return: Movie Object OR None
    """
    # Get movie data_db from imdb movie api
    movie_data = movies_data.get_movies_data(movie_name)

    if movie_data:
        try:
            new_movie_data = Movie(
                title=movie_data['Title'],
                genre=movie_data['Genre'],
                year=movie_data['Year'],
                rating=movie_data['imdbRating'],
                country=movie_data['Country'],
                cover_url=movie_data['Poster'],
                plot=movie_data['Plot'],
                actors=movie_data['Actors'],
                trailer_id=movie_data['imdbID'],
                award=movie_data['Awards'],
                id=new_movie_id(),
                user_id=current_user.id
            )
            return new_movie_data
        except KeyError:
            pass
    return None


@movies_bp.route('<int:user_id>/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie(user_id):
    """
    Route for adding new movies to user's list
    :param user_id: int
    """

    # Gets user instance from the User table
    user = data_manager.get_user_by_id(user_id)
    user_movies = data_manager.get_user_movies(user_id)

    # Handles GET request and displays the add movie form to the user
    if request.method == 'GET':
        return render_template('movies_manager.html', user_movies=user_movies, current_user=current_user)

    # Gets movie_name from the form
    movie_name = request.form.get('movie_name')

    # Gets the new_movie instance (e.g new_movie = Movie(title=tile, rating=rating, ...))
    new_movie_data = get_movies_data(movie_name)

    if new_movie_data:
        # Checks if movie already in the movies table. Just to avoid multiple users adding same movie
        movie_exists = data_manager.get_movie_by_title(new_movie_data.title)

        if movie_exists:
            # Query the UserMovies table to see if the movie is already associated to the user
            # so that a user don't add the same movie that is already in the user's movie list
            user_movie_exists = data_manager.get_movie_from_user_movie_list(user.id, movie_exists.id)
            if user_movie_exists:
                flash(f'The {movie_name} already exists in your favourite movie list add another movie', 'success')

                # Redirect user to user_movies route to  display the list of user's movies
                return redirect(url_for('users.user_movies', user_id=user_id))

            # If a move has been added to the movies table perhaps by another user, then no need to duplicate the
            # movie, just create a relationship between the current user andthe existing movie.
            # Save the user-movie association to the UserMovie table
            user_movie = UserMovie(user=user, movie=movie_exists)

            db.session.add(user_movie)
            db.session.commit()
            flash(f'The {movie_name} has been add to your favourite movie list', 'success')

            # Redirect user to user_movies route to  display the list of user's movies
            return redirect(url_for('users.user_movies', user_id=user_id))

        print(new_movie_data)
        # If its a new movie, then add movie to the Movie Table
        db.session.add(new_movie_data)
        db.session.commit()

        # Create the relationship between the user and new movie in the UserMovie table
        user_movie = UserMovie(user=user, movie=new_movie_data)

        # Save user-movies association to the UserMovie table
        db.session.add(user_movie)
        db.session.commit()

        flash(f'The {movie_name} has been add to your favourite movie list', 'success')

        # Redirect user to user_movies route to  display the list of user's movies
        return redirect(url_for('users.user_movies', user_id=user_id))

    # Else return an error message, movie not found!
    flash(f'The {movie_name} was not found', 'error')

    # Redirect user to user_movies route to  display the list of user's movies
    return render_template('movies_manager.html', user_movies=user_movies, current_user=current_user)


@movies_bp.route('<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def update_movie(user_id, movie_id):
    """
    Route for updating details of a specific movie in a user's movies list
    :param user_id: int
    :param movie_id: int
    """

    # Gets the user-movie object (e.g user_movie = UserMovie(user_id, movie_id))
    # The user_movie object has a reference to both the User and Movie model using the db.backref() function
    user_movie = data_manager.get_movie_from_user_movie_list(user_id, movie_id)

    if request.method == 'GET':
        # Handle GET request and render the update movie html
        return render_template('update_movie.html', user_id=user_id, user_movie=user_movie.movie)

    # Access and update movie properties in movies table through the user_movie instance
    if user_movie:
        user_movie.movie.actors = request.form.get('movie_actors')
        user_movie.movie.genre = request.form.get('movie_genre')
        user_movie.movie.plot = request.form.get('movie_plot')

        # Commit the changes to the database
        db.session.commit()

        flash(f'{user_movie.movie.title} has been updated successfully', 'success')
    else:
        flash(f' The {user_movie.movie.title} is not found in your list of movies', 'success')

        # Redirect user to user_movies route to  display the list of user's movies
        return render_template('movies_manager.html', user_movies=data_manager.get_user_movies(user_id),
                               current_user=current_user)

    # Redirects user to the user movie list page
    return redirect(url_for('users.user_movies', user_id=user_id))


@movies_bp.route('<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(user_id, movie_id):
    """
    Route for deleting a specific movie from a user's list
    :param user_id: int
    :param movie_id: int
    """

    # Get movie to delete
    movie_to_delete = data_manager.get_movie_by_id(movie_id)
    user_movie = data_manager.get_movie_from_user_movie_list(user_id, movie_id)

    if user_movie:
        # Delete User Movie Association (or Relation)
        db.session.delete(user_movie)
        db.session.commit()

        flash(f'{movie_to_delete.title} has been deleted successfully', 'success')
    else:
        flash(f' The {movie_to_delete.title} is not found in your list of movies', 'success')

    # Redirects user to the user movie list page
    return redirect(url_for('users.user_movies', user_id=user_id))


# This route has not been implemented due to time constriants. Will be implemented later on.
@movies_bp.route('<int:user_id>/watched_movie/<int:movie_id>/<string:watched_status>', methods=['POST'])
@login_required
def watched_movie(user_id, movie_id, watched_status):
    """
    Checks and updates the watch status of a specific movie in a user's movies list
    :param user_id: int
    :param movie_id: int
    :param watched_status: string ("YES" or "NO")
    """

    # Fetch user movies
    user_movie = data_manager.get_movie_from_user_movie_list(user_id, movie_id)

    if user_movie:
        if watched_status.lower() == 'no':
            user_movie.watch_status = 'Yes'
            db.session.commit()
        else:
            user_movie.watch_status = 'No'
            db.session.commit()

    # Redirects user to the movies manager page
    return redirect(url_for('movies.add_movie', user_id=user_id))