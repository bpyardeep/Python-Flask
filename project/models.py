from datetime import datetime
from project import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


favourites = db.Table('favourites',
            db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
            db.Column('movie_id',db.Integer,db.ForeignKey('movie_details.movie_id')))


favourites_tv = db.Table('favourites_tv',
            db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
            db.Column('TV_id',db.Integer,db.ForeignKey('TV_details.TV_id')))











class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True)
    comments = db.relationship('Comments',backref='commented_by',lazy=True)
    favourite = db.relationship('Movie_details', secondary=favourites,backref=db.backref('AddToFav'),lazy=True)
    favourite_tv = db.relationship('TV_details', secondary=favourites_tv,backref=db.backref('AddToFavTV'),lazy=True)
    rating = db.relationship('Rating_movie',backref='rated_by',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"


class Post(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(180),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comments',backref='commented_On',lazy=True)


    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"


class Comments(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text,nullable=False)
    date_comment = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'), nullable=False)


class Search_movie_id(db.Model):
    movies_id = db.Column(db.Integer, primary_key=True)





class Movie_details(db.Model):
    movie_id = db.Column(db.Integer,primary_key=True)
    movie_title = db.Column(db.String(200),nullable=False)
    movie_overview = db.Column(db.String(500))
    poster_path = db.Column(db.String(500))
    Popularity = db.Column(db.String(30))
    release_date = db.Column(db.String(30))
    images_list = db.Column(db.String(30))
    actors_list = db.Column(db.String(30))
    trailer = db.Column(db.String(30))
    budget = db.Column(db.Integer)
    homepage = db.Column(db.String(30))
    production_companies = db.Column(db.String(100))
    runtime = db.Column(db.String(30))
    genre = db.Column(db.String(100))
    character = db.Column(db.String(300))
    actor = db.Column(db.String(300))
    actor_id = db.Column(db.String(300))
    actor_image = db.Column(db.String(150),default='default.jpg')
    favourite = db.relationship('User', secondary=favourites,backref=db.backref('AddedToFav'),lazy=True)
    rating = db.relationship('Rating_movie',backref='rated_on',lazy=True)


class TV_details(db.Model):
    TV_id = db.Column(db.Integer,primary_key=True)
    TV_title = db.Column(db.String(200),nullable=False)
    TV_overview = db.Column(db.String(500))
    poster_path = db.Column(db.String(500))
    Popularity = db.Column(db.String(30))
    release_date = db.Column(db.String(30))
    images_list = db.Column(db.String(30))
    actors_list = db.Column(db.String(30))
    trailer = db.Column(db.String(30))
    budget = db.Column(db.Integer)
    homepage = db.Column(db.String(30))
    production_companies = db.Column(db.String(100))
    images_list = db.Column(db.String(30))
    actors_list = db.Column(db.String(30))
    trailer = db.Column(db.String(30))
    genre = db.Column(db.String(100))
    character = db.Column(db.String(300))
    actor = db.Column(db.String(300))
    actor_id = db.Column(db.String(300))
    actor_image = db.Column(db.String(150),default='default.jpg')
    no_of_episodes = db.Column(db.Integer)
    no_of_seasons = db.Column(db.Integer)
    favourites_tv = db.relationship('User', secondary=favourites_tv,backref=db.backref('AddedToFavTV'),lazy=True)

    


class Season_details(db.Model):
    season_id = db.Column(db.Integer, primary_key=True)
    TV_id = db.Column(db.Integer)
    Season_title = db.Column(db.String(200),nullable=False)
    Season_overview = db.Column(db.String(500))
    poster_path = db.Column(db.String(500))
    release_date = db.Column(db.String(30))
    no_of_episodes= db.Column(db.Integer)

















class Actor_details(db.Model):
    actor_id = db.Column(db.Integer, primary_key=True)
    actor_title = db.Column(db.String(200),nullable=False)
    actor_overview = db.Column(db.String(500),nullable=False)
    poster_path = db.Column(db.String(500),nullable=False)
    Popularity = db.Column(db.String(30))
    release_date = db.Column(db.String(30))
    images_list = db.Column(db.String(30))
    actors_list = db.Column(db.String(30))




class Movie_Review(db.Model):
    review_id = db.Column(db.String(100), primary_key=True,nullable=False)
    movie_id = db.Column(db.Integer,nullable=False)
    authour = db.Column(db.String(100))
    review = db.Column(db.String(2000))



class Rating_movie(db.Model):
    rating_id = db.Column(db.String(100),primary_key=True)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    movie_id = db.Column(db.Integer,db.ForeignKey('movie_details.movie_id'),nullable=False)







class SearchDb(db.Model):

    SearchCl = db.Column(db.String(180),primary_key=True)



    def __repr__(self):
        return f"SearchDb('{self.SearchCl}')"
