import tmdbsimple as tmdb
tmdb.API_KEY = '5afe37acf61f67aad9c4a0d5817fa41b'
from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
from imdb import IMDb

from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='28daf694c08240708a7f230a679fdd55')

newsapi.get_top_headlines(q="game of thrones")
newsapi.get_everything(q='movies')['articles']



k = 'tt12345'
k[2:]
movie = tmdb.Movies(278)
mi = movie.info()['imdb_id']
mi['title']

movie_ia = IMDb()
irating = movie_ia.get_movie(mi[2:]).data['rating']
type(irating)


name = mi['title']
name = name.replace("'","")
name = name.replace(":","")
name = name.replace(" ","_")
print(name)

source1 = requests.get('https://www.rottentomatoes.com/m/'+name).text
soup = BeautifulSoup(source1,'lxml')


rating = soup.find('span',class_='mop-ratings-wrap__percentage').text
rating = rating.replace(' ','')
rrating = rating.replace('\n','')
rrating = rrating.replace('%','')
float(rrating)


name1 = mi['title']
name1 = name1.replace("'","")
name1 = name1.replace(":","")
name1 = name1.replace(" ","-")
name1 = name1.lower()
url = 'https://www.metacritic.com/movie/'+name1

req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
webpage = urlopen(req).read()


soup1 = BeautifulSoup(webpage,'lxml')
soup1.find('div',class_='metascore_w larger movie positive').text
mtrating = soup1.find('div',class_='metascore_w user larger movie positive').text

float(mtrating)