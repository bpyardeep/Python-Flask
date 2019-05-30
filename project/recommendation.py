# import pandas as pd
# import sqlite3

# con = sqlite3.connect("project/site.db")
# movies = pd.read_sql_query("SELECT * from movie_details", con)
# con.close()


# user_rating = pd.read_sql_query("SELECT * from rating_movie",con)
# data1 = pd.merge(movies,user_rating,on="movie_id")


# data1.groupby('movie_title')['rating'].count().sort_values(ascending=False).head()



# # creating dataframe with 'rating' count values 
# ratings = pd.DataFrame(data1.groupby('movie_title')['rating'].mean()) 

# ratings['num of ratings'] = pd.DataFrame(data1.groupby('movie_title')['rating'].count()) 

# ratings.head() 



# # Sorting values according to 
# # the 'num of rating column' 
# moviemat = data1.pivot_table(index ='user_id', 
# 			columns ='movie_title', values ='rating') 

# moviemat.head() 

# ratings.sort_values('num of ratings', ascending = False).head(10) 


# # analysing correlation with similar movies 
# starwars_user_ratings = moviemat['Star Wars'] 
# liarliar_user_ratings = moviemat['Liar Liar'] 

# starwars_user_ratings.head() 




# # analysing correlation with similar movies 
# similar_to_starwars = moviemat.corrwith(starwars_user_ratings) 
# similar_to_liarliar = moviemat.corrwith(liarliar_user_ratings) 

# corr_starwars = pd.DataFrame(similar_to_starwars, columns =['Correlation']) 
# corr_starwars.dropna(inplace = True) 

# corr_starwars.head() 





# # Similar movies like starwars 
# corr_starwars.sort_values('Correlation', ascending = False).head(10) 
# corr_starwars = corr_starwars.join(ratings['num of ratings']) 

# corr_starwars.head() 

# corr_starwars[corr_starwars['num of ratings']>100].sort_values('Correlation', ascending = False).head() 
