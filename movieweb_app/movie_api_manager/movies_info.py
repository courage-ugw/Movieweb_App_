class MoviesInfo:
    """
    The class returns pieces of information associated to a list of movie objects
    """
    def __init__(self, movies_lst: list[object]):
        self._movies = movies_lst

    @property
    def total_favourite_movies(self):
        """
        returns the length of the list of movie objects
        :return:
            total_favourite_movies: int
        """
        return len(self._movies)

    @staticmethod
    def is_highly_rated(rating):
        """
        Returns True if a movie rating is greater than 7 else false
        :param rating: int or float
        :return: True or False
        """
        return rating != 'N/A' and float(rating) > 7

    @property
    def high_rated_movies(self):
        """
        counts the sum of all highly rated movies and returns the value
        :return:
            high_rated_movies_count: int
        """
        high_rated_movies_count = sum([1 for movie in self._movies if self.is_highly_rated(movie.rating)])
        return high_rated_movies_count

    @property
    def worst_movie_rating(self):
        """
        Checks the movie ratings and returns the minimum rating. If no rating, it returns None
        :return:
            Minimum rating value: int or float OR None
        """
        movie_ratings = [float(movie.rating) for movie in self._movies if movie.rating != 'N/A']
        return min(movie_ratings, default=None)

    @property
    def recent_movie_release(self):
        """
        Checks for the sum of all recent movies.
        :return:
            recent_movie_release_count: int
        """
        recent_movie_release_count = sum([1 for movie in self._movies if self.is_a_recent_release(movie.year)])
        return recent_movie_release_count

    @staticmethod
    def is_a_recent_release(year):
        """
        Returns true if a movie year is beyond 2021, else false
        :param year: string (as year range (2020-2022 or single year (2022))
        :return: True or False
        """
        # if we have a year range (e.g 2010-2020), then split using "-" and convert the result to integer
        if "–" in year:
            movie_year_earliest, movie_year_latest = list(map(int, year.split("–")))
            return movie_year_latest > 2021 if movie_year_latest else movie_year_earliest > 2021

        return int(year) > 2021

    @property
    def total_movies_watched(self):
        """
        Returns the value of the movie watched
        :return: watched_count: int
        """

        # watched_movies_count = sum([1 for movie in self._movies if self.is_watched(movie.watch)])
        # return watched_movies_count
        return 0

    # @staticmethod
    # def is_watched(watch_status):
    #     return watch_status.lower() == 'yes'

    @property
    def total_movies_with_award(self):
        """
        Returns the summed value of all movies with award.
        :return: movies_with_award_count: int
        """
        movies_with_award_count = sum([1 for movie in self._movies if self.movie_award(movie.award)])
        return movies_with_award_count

    @staticmethod
    def movie_award(award):
        """
        Returns True if a movie award exits, else if movie award is ''n/a' or empty, returns False
        :param award: string
        :return: True or False
        """
        return award.lower() != 'n/a' or award.lower() != ''

    @property
    def movies_count_by_countries(self):
        """
        Returns a list of tuples of top 2 countries based on their frequency.
        :return: movies_country_count: list[('US', 3), ('UK', 4)]
        """
        movies_country_count = {}

        for movie in self._movies:
            countries = [country.strip() for country in movie.country.split(',')]
            for country in countries:
                movies_country_count[country] = movies_country_count.get(country, 0) + 1

        return sorted(movies_country_count.items(), key=lambda item: item[1], reverse=True)[:2]

    @property
    def top_rated_movie_name(self):
        """
        Returns a list of tuple containing the top rated movie. if no movie, returns an empty list
        :return: list[('Game of Thrones', 7)] OR []
        """
        movies_and_ratings = {}

        for movie in self._movies:
            if movie.rating != 'N/A' and movie.title not in movies_and_ratings:
                movies_and_ratings[movie.title] = float(movie.rating)

        if movies_and_ratings:
            return sorted(movies_and_ratings.items(), key=lambda item: item[1], reverse=True)[0]

        return []