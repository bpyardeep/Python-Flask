import tmdbsimple as tmdb
tmdb.API_KEY = '5afe37acf61f67aad9c4a0d5817fa41b'
import pandas as pd
from project.models import Search_movie_id,Movie_details,Movie_Review
from project import db



class DisplayMovies():
    def __init__(self,id):
        self.movies_list = []
        self.id = id
        self.Images = []
        self.Actors = []
        self.pc = []
        self.genre = []
        self.Actor_list = []
        self.Character_list = []
        self.actor_id = []
        self.actor_image = []



        movie = tmdb.Movies(self.id)
        actors = movie.credits()['cast'][:10]

        for i in actors:
            self.Actors.append(i['credit_id'])
        actors = '$'.join(self.Actors)

        images = movie.images()['backdrops'][:10]

        for i in images:
            self.Images.append(i['file_path'])
        images_1 = '$'.join(self.Images)

        if len(movie.videos()['results']) > 0:
            trailer = movie.videos()['results'][0]['key']
        else:
            trailer = 'None'


        self.response = movie.info()

        for i in self.response['production_companies']:
            self.pc.append(i['name'])




        for i in self.response['genres']:
            self.genre.append(i['name'])





        ActorCharacter = (movie.credits()['cast'][:10])

        for i in ActorCharacter:
            self.Actor_list.append(i['name'])
            self.Character_list.append(i['character'])
            self.actor_id.append(str(i['id']))
            if i['profile_path'] == None:
                self.actor_image.append('None')
            else:
                self.actor_image.append(i['profile_path'])


        Movies_details = Movie_details(movie_id=self.response['id'],
                                        movie_title=self.response['original_title'],
                                        movie_overview=self.response['overview'],
                                        poster_path=self.response['poster_path'],
                                        Popularity=str(self.response['vote_average']),
                                        release_date=self.response['release_date'],
                                        images_list=images_1,
                                        actors_list=actors,
                                        trailer=trailer,
                                        budget=self.response['budget'],
                                        homepage=self.response['homepage'],
                                        production_companies= '$'.join(self.pc),
                                        runtime = self.response['runtime'],
                                        genre="$".join(self.genre),
                                        character = '$'.join(self.Actor_list),
                                        actor = '$'.join(self.Character_list),
                                        actor_id = '$'.join(self.actor_id),
                                        actor_image = '$'.join(self.actor_image)
                                        )
        db.session.add(Movies_details)
        db.session.commit()









        #self.movies_list.append([response['id'],response['original_title'],response['poster_path'],response['overview'],response['release_date'],response['vote_average']])


class SearchForMovies():
    movies_list = []

    def __init__(self,keyword):

        self.keyword=keyword
        search = tmdb.Search()
        self.movies_id = search.movie(query=self.keyword)['results'][:10]


    def loadingIntoDatabase(self):
        for i in self.movies_id:
            if db.session.query(Movie_details.movie_id).filter_by(movie_id=i['id']).scalar() is None:
                DM = DisplayMovies(i['id'])

    def loadReviewsIntoDatabase(self,id):
        movie = tmdb.Movies(id)
        reviews = movie.reviews(Page=1)['results']
        for i in reviews:
             if db.session.query(Movie_Review.review_id).filter_by(review_id=i['id']).scalar() is None:

                movie_Review = Movie_Review(review_id=i['id'],
                                            movie_id=id,
                                            authour=i['author'],
                                            review=i['content'])
                db.session.add(movie_Review)
        db.session.commit()




class ActorCharacter():

    def __init__(self,character_id):

        movie = tmdb.Credits(character_id)
        self.name = movie.info()['person']['name']
        self.character = movie.info()['media']['character']







        # for i in self.details:
        #     self.l.append([i['id'],i['title'],i['poster_path'],i['overview'],i['release_date'],i['vote_average']])
