import requests


class MovieDataFetcher:
    """
    The MovieDataFetcher Class interacts with the imdB API and fetches the movie data.
    It also fetches country alpha code, given a country name.
    """

    def __init__(self):
        """ class constructor """
        self._request_url = 'https://www.omdbapi.com/?apikey=eb462b7d&t='
        self._request_url_country = "https://rest-countries10.p.rapidapi.com/country/"
        self._headers = {
            "X-RapidAPI-Key": "9bcf117f10msh4043aa916958825p12243fjsnd31208cf6b30",
            "X-RapidAPI-Host": "rest-countries10.p.rapidapi.com"
        }

    def get_movies_data(self, movie_name):
        """
        Makes request to the movie API and returns fetched movie data as JSON
        :param movie_name: string
        :return: JSON or None
        """
        try:
            url = self._request_url + movie_name
            return requests.get(url).json()
        except KeyError:
            return None

    def get_country_alpha_code(self, country_name):
        """
        Fetches a country's alpha code using a country name
        :param country_name:
        :return: country short code as string (e.g. NIG for Nigeria, USA for United States of America)
        """
        try:
            url = self._request_url_country + country_name
            response = requests.get(url, headers=self._headers).json()
            return response[0]['code']['alpha3code']
        except KeyError:
            return None
        except IndexError:
            return None