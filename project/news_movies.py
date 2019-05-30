from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='28daf694c08240708a7f230a679fdd55')





class Get_news():
    def __init__(self,keyword='movies'):
        self.default = newsapi.get_everything(q=keyword)['articles']
