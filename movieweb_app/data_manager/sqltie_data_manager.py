from movieweb_app.models import User, Movie, UserMovie, UserMovieAcitivity
from movieweb_app.data_manager.data_manager_interface import DataManagerInterface
from movieweb_app import db

class SQLiteDataManager(DataManagerInterface):

    def create_tables(self, app):
        with app.app_context():
            db.create_all()

    @property
    def all_users(self):
        """
        Queries the User table
        :return:
            list of User Objects
            users: List[User(id=1, username='John Doe', email='johndoe@gmail.com'), User(id=1,...),... ]
        """
        return User.query.all()

    @property
    def all_movies(self):
        """
        Queries the Movies table
        :return:
            list of Movies Objects
            movies: List[Movie(id=1, title='John Wick', rating=8.5), User(id=1,...),... ]
        """
        return Movie.query.all()

    def get_user_by_id(self, user_id):
        """
        Returns a user objec, given a user id
        :param user_id: int(user id)
        :return: User Object (User(id=user_id, name=user name, username=username, ...))
        """
        return db.session.get(User, user_id)

    def get_user_by_email(self, email):
        """
        Returns a user object, given an email
        :param email: string
        :return: User Object (User(id=user_id, name=user name, username=username, ...))
        """
        return User.query.filter(User.email == email).first()

    def get_user_by_username(self, username):
        """ """
        return User.query.filter(User.username == username).first()

    def get_user_movies(self, user_id):
        """
        Queries the DB for user movies and returns list of movies for a particular user
        :param:
            user_id: int
        :return:
            list of movie objects.
            movies: List[movie_object1, movie_object2, ...]
        """
        user_movies = UserMovie.query.filter_by(user_id=user_id).all()
        movies = [user_movie.movie for user_movie in user_movies]
        return movies

    def get_movie_by_id(self, movie_id):
        """ Return a user with a given user_id """
        return db.session.get(Movie, movie_id)

    def get_movie_by_title(self, movie_title):
        """
        Returns a movie object by querying the movies table using a movie title
        :param movie_title: string
        :return: Movie Object (e.g Movie(title=tile, rating=rating, ...))
        """
        return Movie.query.filter_by(title=movie_title).first()

    def get_movie_from_user_movie_list(self, user_id, movie_id):
        """
        Returns a specific movie object that is associated to a specific user, given both user id and movie id
        :param user_id: int
        :param movie_id: int
        :return: Movie Object
        """
        user_movie = UserMovie.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        return user_movie

    def get_user_movie_activity(self, user_id, movie_id):
        activity = UserMovieAcitivity.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        return activity