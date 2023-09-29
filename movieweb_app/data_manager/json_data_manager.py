import json
from os.path import dirname, join, exists
from .data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    # Root Path to the file folder
    _project_root = dirname(dirname(__file__))

    def __init__(self, filename):
        file_path = join(self._project_root, 'data', filename)
        self.filename = file_path

    def create_file(self):
        """ Creates file if file does not exist. If file exists, do nothing"""
        if not exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump([], file)

    @property
    def all_users(self):
        """ Loads file and returns all users """

        # If file does not exists, create the file, else do nothing
        self.create_file()

        try:
            with open(self.filename, 'r') as json_file:
                data = json.load(json_file)
            return data
        except json.JSONDecodeError as e:
            print("JSON Decode Error: {e}")
            return None

    def get_user_movies(self, user_id):
        """ Return a list of all movies for a given user """
        users = self.get_all_users

        for user in users:
            if user['id'] == user_id:
                return user['movies']

    def get_user_by_id(self, user_id):
        """ Return a user with a given user_id """
        users = self.get_all_users
        for user in users:
            if user['id'] == user_id:
                return user
        # If user not found, return None
        return None

    def get_user_by_username(self, username):
        """ """
        users = self.get_all_users
        for user in users:
            if user['username'] == username:
                return user
        return None

    def get_user_by_email(self, email):
        """ """
        users = self.get_all_users
        for user in users:
            if user["email"] == email:
                return user
        return None

    def save_user(self, user):
        """ Saves users to the Json file """

        users = self.get_all_users
        users.append(user)

        with open(self.filename, 'w') as file:
            json.dump(users, file, indent=4)

    def save_users(self, users):
        """ Saves users to the Json file """

        with open(self.filename, 'w') as file:
            json.dump(users, file, indent=4)

    def save_user_movies(self, user_movies, user_id):
        """ Saves users to the Json file """

        users = self.get_all_users
        for user in users:
            if user['id'] == user_id:
                user['movies'] = user_movies

        with open(self.filename, 'w') as file:
            json.dump(users, file, indent=4)