from flask_login import UserMixin
from movieweb_app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    # Load the user from your database using the user_id
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    like_count = db.Column(db.Integer, default=0, nullable=False)
    date_registered = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}')"


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trailer_id = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    cover_url = db.Column(db.String, nullable=False)
    award = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    plot = db.Column(db.Text, nullable=False)
    year = db.Column(db.String, nullable=False)
    actors = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Movie(id={self.id}, title='{self.title}', year={self.year}, cover_url='{self.cover_url}', country='{self.country}')"


class UserMovie(db.Model):
    __tablename__ = 'user_movies'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('user_movies', cascade='all, delete-orphan'))
    movie = db.relationship('Movie', backref=db.backref('movie_users', cascade='all, delete-orphan'))


class UserMovieAcitivity(db.Model, UserMixin):
    __tablename__ = 'user_movie_activities'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    watch_status = db.Column(db.String, default='No', nullable=False)
    review = db.Column(db.Text)

    def __repr__(self):
        return f"UserMovieActivity(user_id={self.user_id}, movie_id={self.movie_id}, watch_status=" \
               f"'{self.watch_status}', review='{self.review}')"