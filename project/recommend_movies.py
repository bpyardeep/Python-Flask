import tmdbsimple as tmdb
tmdb.API_KEY = '5afe37acf61f67aad9c4a0d5817fa41b'


class recommend():
    def __init__(self,id):
        movie = tmdb.Movies(id)
        self.recom_movies = movie.recommendations(page=1)['results']

        