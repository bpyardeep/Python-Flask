import tmdbsimple as tmdb
tmdb.API_KEY = '5afe37acf61f67aad9c4a0d5817fa41b'
from imdb import IMDb
from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen





class Compare_movies():
    def __init__(self,id):
        self.id = id
        movie = tmdb.Movies(id)
        
        movie_ia = IMDb()
        self.image = movie.info()['poster_path']
        imdb_id = movie.info()['imdb_id']
        self.imdb_rating = movie_ia.get_movie(imdb_id[2:]).data['rating']
    


    def rotten_tomatoes(self):
        movie = tmdb.Movies(self.id)
        mi = movie.info()
        name = mi['title']
        self.title = mi['title']

        try:
            name = name.replace("'","")
            name = name.replace(":","")
            name = name.replace(" ","_")
            source1 = requests.get('https://www.rottentomatoes.com/m/'+name).text
            soup = BeautifulSoup(source1,'lxml')


            rating = soup.find('span',class_='mop-ratings-wrap__percentage').text
            rating = rating.replace(' ','')
            self.rotten_rating = rating.replace('\n','')
            self.rotten_rating = rating.replace('%','')
        except:
            self.rotten_rating ="{0:.0f}".format((self.imdb_rating * 1.034)*10) 

    def metacritic(self):
        
        name1 = self.title
        name1 = name1.replace("'","")
        name1 = name1.replace(":","")
        name1 = name1.replace(" ","-")
        name1 = name1.lower()
        url = 'https://www.metacritic.com/movie/'+name1

        req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
        try:
            webpage = urlopen(req).read()
            soup1 = BeautifulSoup(webpage,'lxml')
            self.critic_meta = soup1.find('div',class_='metascore_w larger movie positive').text
        except:
            self.critic_meta = "{0:.0f}".format(self.imdb_rating * 0.94) 


    def Compute_final(self):
        if self.critic_meta == 'Nan':
            self.critic_meta = 3.6
        
        self.final_rating = (((self.imdb_rating*5.67) + ((float(self.rotten_rating)/10)*4.43) + ((float(self.critic_meta)/10)*3.56))/136.6)*100
        self.final_rating = "{0:.2f}".format(self.final_rating)

        
        
    



