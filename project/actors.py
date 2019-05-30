import tmdbsimple as tmdb
tmdb.API_KEY = '5afe37acf61f67aad9c4a0d5817fa41b'

class SearchForActors():
    def __init__(self,keyword):
        self.l = []
        self.m = []
        self.keyword = keyword
        search = tmdb.Search()
        response = search.person(query=self.keyword)
        for i in response['results']:
            search1 = tmdb.People(i['id']).info()
            self.l.append([search1['id'],search1['name'],search1['biography'],search1['place_of_birth'],search1['birthday'],search1['popularity'],search1['profile_path']])
