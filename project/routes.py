import secrets
import os
import json
from PIL import Image
from flask import render_template,url_for,flash,redirect,request,jsonify,abort
from project import app,db,bcrypt
from project.forms import RegistrationForm,LoginForm,MovieSearchForm, UpdateAccountForm,PostForm,SearchForm,CommentForm,Favourite_form,CompareForm,NewsForm
from project.models import SearchDb,User,Post,Comments,Movie_details,TV_details,Season_details,favourites,Movie_Review,Rating_movie
from flask_login import login_user,current_user,logout_user, login_required
from project.movies import SearchForMovies,DisplayMovies,ActorCharacter
from project.tv import SearchForTv,DisplayTV
from project.recommend_movies import recommend
from project.compare import Compare_movies
from project.news_movies import Get_news
from project.new_release import Display_new_content
from project.actors import SearchForActors
from sqlalchemy import select,asc
from project.errors.handlers import error_403,error_404,error_500


@app.route("/favourites",methods=['GET','POST'])
def favourites():
    movies = []
    TVS = []
    favourite_content = current_user.AddedToFav
    
    for i in favourite_content:
        movie_id = i.movie_id
        movie = Movie_details.query.get_or_404(movie_id)
        movies.append(movie)

    movies.reverse()

    favourite_content_tv = current_user.AddedToFavTV
    for i in favourite_content_tv:
        TV_id = i.TV_id
        TV = TV_details.query.get_or_404(TV_id)
        TVS.append(TV)

    return render_template('favourites.html',movies= movies,TVS=TVS)






@app.route("/_favouritess/<int:type>/<movie_id>",methods=['GET','POST'])
def _favouritess(movie_id,type):
    if type == 1:
        movie = Movie_details.query.get_or_404(movie_id)
        movie.AddToFav.append(current_user)
        db.session.commit()
        return "-"
        
    if type == 2:
        k = current_user.AddedToFav
        for i in k:
            if i.movie_id == int(movie_id):
                k.remove(i)
                
                break
        db.session.commit()
        return "-"
        


@app.route("/_favouritess_tv/<int:type>/<TV_id>",methods=['GET','POST'])
def _favouritess_tv(TV_id,type):
    if type == 1:
        TV = TV_details.query.get_or_404(TV_id)
        TV.AddToFavTV.append(current_user)
        db.session.commit()
        return "_"
        
    if type == 2:
        k = current_user.AddedToFavTV
        for i in k:
            if i.TV_id == int(TV_id):
                k.remove(i)
                
                break
        db.session.commit()
        return "-"


     

@app.route('/_star_rating_movie/<int:stars>/<movie_id>',methods=['GET','POST'])
def _star_rating_movie(stars,movie_id):
    movie = Movie_details.query.get_or_404(movie_id)
    random_review_id = str(movie.movie_id)+"$"+str(current_user.id)
    if db.session.query(Rating_movie.rating_id).filter_by(rating_id=random_review_id).scalar() is None:
        rating_movie = Rating_movie(rating_id = random_review_id,rating=stars,rated_by=current_user,rated_on=movie)
        db.session.add(rating_movie)
        db.session.commit()
        return render_template('home.html')
    return "_hello"
        
        









@app.route('/auto')
def autocomplete():
    try:
        form = SearchForm()
        if form.validate_on_submit():
            movie = ['Hellboy','Student of the year','Avengers']
            return render_template('testing.html',form = form,movies_names=movie)

        return render_template('testing.html',form = form,movies_names=movies_names)
    except :
        flash("sorry This Page is UnderConstruction","warning")
        return render_template('home.html')

@app.route('/recommending')
def recommending():
    favourite_content = current_user.AddedToFav
    favourite_content.reverse()
    favvs = []
    for i in favourite_content:
        fav = recommend(i.movie_id)
        favs = fav.recom_movies
        favvs.append(favs)
        
    return render_template('recommend.html',favs = favvs)


@app.route('/home')
def home():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=10)
    
    return render_template('home.html',posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/',methods=['get','post'])
def index():
    form = NewsForm()
    if form.validate_on_submit():
        keyword = form.search_new.data
        news = Get_news(keyword)
        news_movies = news.default
        return render_template('updates.html',form=form,searched_news = news_movies)
        
    news_movies = Get_news()
    news = news_movies.default
    return render_template('updates.html',form=form, news= news)



@app.route('/loadMovies',methods=['GET','POST'])
@login_required
def loadMovies():
    form = MovieSearchForm()
    if form.validate_on_submit():
        if form.select.data == 'Movie':
            search_text = form.search_movies.data
            s = SearchForMovies(search_text)
            
            try:
                s.loadingIntoDatabase()
            except:
                flash('Something happened','warning')
            for i in s.movies_id:
                s.loadReviewsIntoDatabase(i['id'])
            if len(s.movies_id) == 0:
                flash(f'No result found','danger')
        elif form.select.data == 'TV':
            search_text = form.search_movies.data
            s = SearchForTv(search_text)
            s.loadingIntoDatabase()
            s.loadSeasonsIntoDataBase(s.TV_id[0]['id'])
            if len(s.TV_id) == 0:
                flash(f'No result found','danger')


            return render_template('load_movies.html',title='Movies', form=form)

    return render_template('load_movies.html',title='Movies', form=form)





@app.route('/movies',methods=['GET','POST'])
@login_required
def movies():



    form = MovieSearchForm()
    if form.validate_on_submit():
        if form.select.data == 'Movie':
            search_text = form.search_movies.data
            s = SearchForMovies(search_text)
            return render_template('movies.html',title='Movies', form=form,movies=s.movies_id)


        elif form.select.data == 'TV':
            search_text = form.search_movies.data
            s = SearchForTv(search_text)
            return render_template('movies.html',title='Tv', form=form,tvs=s.TV_id)


        elif form.select.data == 'Actor':
            search_text = form.search_movies.data
            s = SearchForActors(search_text)
            if len(s.l) == 0:
                flash(f'No result found','danger')

            return render_template('movies.html',title='Tv', form=form,actors=s.l)

        flash(f"No Movie Found","danger")
    return render_template('movies.html',title='Movies', form=form)





@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! you are now able to log in','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)






@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')

            flash(f'Welcome back {user.username}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        flash(f'Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)





@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pic',picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)


    return picture_fn


@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated','success')
        return redirect(url_for('account'))


    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static',filename = 'profile_pic/'+ current_user.image_file)
    return render_template('account.html',title='Account', image_file=image_file, form=form)



@app.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('home'))

    return render_template('create_post.html',title='New Post', form=form,legend="New Post")




@app.route("/moviesResult/<int:type>/<movie_id>")
def moviesResult(movie_id,type):
    if type == 1:
        star_rating = Rating_movie.query.filter_by(rating_id=str(movie_id)+"$"+str(current_user.id)).all()
            
        favs = current_user.AddedToFav
        movie = Movie_details.query.get_or_404(movie_id)
        reviews = Movie_Review.query.filter_by(movie_id=movie_id).all()
        images_poster = movie.images_list.split('$')
        charact = movie.character.split('$')
        act = movie.actor.split('$')
        act_img = movie.actor_image.split('$')
        charactactor = []
        for i in range(len(act)):
            charactactor.append([charact[i],act[i],act_img[i]])
        pcs = movie.production_companies.replace("$",",")
        genre_str = movie.genre.replace('$',',')
        AddedFav = False
        for fav in favs:
            if fav.movie_id == int(movie_id):
                AddedFav = True
                break
            else:
                AddedFav = False

        

        
        return render_template("moviesResult.html",
                                title='Movies Result',
                                movie = movie,
                                images=images_poster,
                                video=movie.trailer,
                                casts = charactactor,
                                budget=movie.budget,
                                homepage=movie.homepage,
                                pcs = pcs,
                                runtime = movie.runtime,
                                genre = genre_str,
                                movie_idd = movie_id,
                                Favv = AddedFav,
                                reviews = reviews,
                                rating = star_rating)
    elif type == 2:
        favs = current_user.AddedToFavTV
        TV = TV_details.query.get_or_404(movie_id)
        SEASON = Season_details.query.filter_by(TV_id=movie_id).all()
        images_poster = TV.images_list.split('$')
        charact = TV.character.split('$')
        act = TV.actor.split('$')
        act_img = TV.actor_image.split('$')
        pcs = TV.production_companies.replace("$",", ")
        charactactor = []
        for i in range(len(act)):
            charactactor.append([charact[i],act[i],act_img[i]])

        genre_str = TV.genre.replace('$',',')
        
        AddedFav = False
        for fav in favs:
            if fav.TV_id == int(movie_id):
                AddedFav = True
                break
            else:
                AddedFav = False
        return render_template("tvResult.html",
                                title='Movies Result',
                                TV = TV,
                                images=images_poster,
                                video=TV.trailer,
                                casts = charactactor,
                                homepage=TV.homepage,
                                pcs = pcs,
                                genre = genre_str,
                                seasons = SEASON,
                                Favv = AddedFav)

    return render_template("moviesResult.html"
                            )


@app.route('/post/<int:post_id>',methods=['GET','POST'])
def post(post_id):

    form = CommentForm()
    if form.validate_on_submit():
        post = Post.query.get_or_404(post_id)
        
        comment = Comments(content=form.content.data,commented_by=current_user,commented_On=post)
        db.session.add(comment)
        db.session.commit()
        flash('Comment Added','success')
        comments = Comments.query.filter_by(post_id=post_id).all()
        return render_template('post.html',title=post.title,post=post,form=form,comments=comments)
    post = Post.query.get_or_404(post_id)

    return render_template('post.html',title=post.title,post=post,form=form,comments= Comments.query.filter_by(post_id=post_id).all())

@app.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been Updated!','success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method == "GET":

        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',
                          title='Update Post', 
                                form=form,
                                legend="Update Post")


@app.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    comments = Comments.query.filter_by(post_id=post_id).all()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    for i in comments:
        db.session.delete(i)
    db.session.delete(post)
    
    db.session.commit()
    flash('Your post has been deleted','success')
    return redirect(url_for('home'))







@app.route('/new_release')
def new_release():
    s = Display_new_content()
    movies = s.latest_movie
    tvs = s.latest_tv


    return render_template('new_release.html',movies=movies,tvs=tvs)



@app.route('/user/<username>')
def user_post(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page',1,type=int)
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc())\
                            .order_by(Post.date_posted.desc())\
                            .paginate(page=page,per_page=10)
    
    return render_template('user_post.html',posts=posts,user=user)



@app.route('/compare_movies',methods=['GET','POST'])
def compare_movies():
    form = CompareForm()
    if form.validate_on_submit():
        movie_1_id = form.movie_1.data
        movie_2_id = form.movie_2.data
        movie_1 = Compare_movies(movie_1_id)

        movie_1.rotten_tomatoes()
        
        movie_1.metacritic()
        movie_1.Compute_final()
        
        
        
        
        movie_2 = Compare_movies(movie_2_id)
        movie_2.rotten_tomatoes()
        movie_2.metacritic()
        movie_2.Compute_final()
        
        
        
        movie_1_dic = {
            'imdb_rating': movie_1.imdb_rating,
            'rotten_rating':movie_1.rotten_rating,
            'meta_crtic_rating':movie_1.critic_meta,
            'final_rating': movie_1.final_rating,
            'poster_path': movie_1.image,
            'title': movie_1.title,
            'float_rating':float( movie_1.final_rating)
            
        }

        movie_2_dic = {
            'imdb_rating': movie_2.imdb_rating,
            'rotten_rating':movie_2.rotten_rating,
            'meta_crtic_rating':movie_2.critic_meta,
            'final_rating': movie_2.final_rating,
            'poster_path': movie_2.image,
            'title': movie_2.title,
            'float_rating':float( movie_1.final_rating)
        }
        return render_template('compare_movies.html',form=form,movie1=movie_1_id,
                                                                movie2=movie_2_id,
                                                                movie_1_rating = movie_1_dic,
                                                                movie_2_rating=movie_2_dic)

    return render_template('compare_movies.html',form=form)



@app.route('/_comparing/<movie1_id>/<movie2_id>',methods=['GET','POST'])
def _comparing(movie1_id,movie2_id):
    movie_1 = Compare_movies(movie1_id)
    movie_1.rotten_tomatoes()
    movie_1.metacritic()
    movie_1.Compute_final()
    movie_1.final_rating
    movie_2 = Compare_movies(movie2_id)
    movie_2.rotten_tomatoes()
    movie_2.metacritic()
    movie_2.Compute_final()
    movie_2.final_rating
    
    
    
    movie_1_dic = {
        'imdb_rating': movie_1.imdb_rating,
        'rotten_rating':movie_1.rotten_rating,
        'meta_crtic_rating':movie_1.critic_meta,
        'meta_user_rating':movie_1.user_meta
    }

    movie_2_dic = {
        'imdb_rating': movie_2.imdb_rating,
        'rotten_rating':movie_2.rotten_rating,
        'meta_crtic_rating':movie_2.critic_meta,
        'meta_user_rating':movie_2.user_meta
    }
    return render_template('compare_movies.html',movie_1_rating = movie_1_dic,movie_2_rating=movie_2_dic)
