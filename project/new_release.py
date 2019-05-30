import tmdbsimple as tmdb
tmdb.API_KEY = '5afe37acf61f67aad9c4a0d5817fa41b'

class Display_new_content():
    def __init__(self):
        latest = tmdb.Discover()
        self.latest_movie = latest.movie()['results'][:20]
        self.latest_tv = latest.tv()['results'][:20]






        