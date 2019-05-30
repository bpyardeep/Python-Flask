import tmdbsimple as tmdb
tmdb.API_KEY = '5afe37acf61f67aad9c4a0d5817fa41b'
from project.models import Search_movie_id,TV_details,Season_details
from project import db




class DisplayTV():
    def __init__(self,id):


        self.TV_list = []
        self.id = id
        self.Images = []
        self.Actors = []
        self.pc = []
        self.genre = []
        self.networks = []
        self.Actor_list = []
        self.Character_list = []
        self.actor_id = []
        self.actor_image = []



        TV = tmdb.TV(self.id)
        actors = TV.credits()['cast'][:10]

        for i in actors:
            self.Actors.append(i['credit_id'])
        actors = '$'.join(self.Actors)

        images = TV.images()['backdrops'][:10]

        for i in images:
            self.Images.append(i['file_path'])
        images_1 = '$'.join(self.Images)

        if len(TV.videos()['results']) > 0:
            trailer = TV.videos()['results'][0]['key']
        else:
            trailer = 'None'


        self.response = TV.info()

        for i in self.response['production_companies']:
            self.pc.append(i['name'])


        for i in self.response['networks']:
            self.networks.append(i['name'])

        for i in self.response['genres']:
            self.genre.append(i['name'])





        ActorCharacter = (TV.credits()['cast'][:15])

        for i in ActorCharacter:
            self.Actor_list.append(i['name'])
            self.Character_list.append(i['character'])
            self.actor_id.append(str(i['id']))
            if i['profile_path'] == None:
                self.actor_image.append('None')
            else:
                self.actor_image.append(i['profile_path'])


        TV_detail = TV_details(TV_id=self.response['id'],
                                        TV_title=self.response['original_name'],
                                        TV_overview=self.response['overview'],
                                        poster_path=self.response['poster_path'],
                                        Popularity=str(self.response['vote_average']),
                                        release_date=self.response['first_air_date'],
                                        images_list=images_1,
                                        actors_list=actors,
                                        trailer=trailer,
                                        homepage=self.response['homepage'],
                                        production_companies= '$'.join(self.pc),
                                        genre="$".join(self.genre),
                                        character = '$'.join(self.Actor_list),
                                        actor = '$'.join(self.Character_list),
                                        actor_id = '$'.join(self.actor_id),
                                        actor_image = '$'.join(self.actor_image),
                                        no_of_episodes=self.response['number_of_episodes'],
                                        no_of_seasons=self.response['number_of_seasons']
                                        )
        db.session.add(TV_detail)
        db.session.commit()

    





class SearchForTv():

    def __init__(self,keyword):

        self.keyword=keyword
        search = tmdb.Search()
        self.TV_id = search.tv(query=self.keyword)['results'][:1]


    def loadingIntoDatabase(self):
        for i in self.TV_id:
            self.tv__id = i['id']
            if db.session.query(TV_details.TV_id).filter_by(TV_id=i['id']).scalar() is None:
                DT = DisplayTV(i['id'])
            
    
    def loadSeasonsIntoDataBase(self,id):
        tv = tmdb.TV(id)    
        self.seasons = tv.info()['seasons']
        for j in self.seasons:
            if db.session.query(Season_details.season_id).filter_by(season_id=j['id']).scalar() is None:


                season_detail = Season_details(season_id=j['id'],
                                                TV_id = self.tv__id,
                                                Season_title=j['name'],
                                                Season_overview=j['overview'],
                                                poster_path=j['poster_path'],
                                                release_date=j['air_date'],
                                                no_of_episodes=j['episode_count'],
                                                )
                db.session.add(season_detail)
                db.session.commit()