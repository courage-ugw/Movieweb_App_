import os

# get the path to the database file
root_dir = os.path.dirname(__file__)
db_file_path = os.path.join(root_dir, 'data', 'movie_app.sqlite')

class Config:
    SECRET_KEY = '5722f4a3deabe7bb'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_file_path