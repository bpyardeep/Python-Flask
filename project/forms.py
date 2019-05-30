from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField, SubmitField,BooleanField,SelectField, TextAreaField,TextField, IntegerField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError,NumberRange
from project.models import User

'''
This class is for Registration
Here we have username,Email,Password, confirmPassword and submit button
We have applied Some Validators as well from the above Modules E.g wtform.validators
'''
class RegistrationForm(FlaskForm):
    username = StringField('username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',
                        validators=[DataRequired(),Email()])
    password = PasswordField('New Password',validators=[DataRequired(),EqualTo('confirm_password', message='Passwords must match')])

    confirm_password = PasswordField('Repeat Password')

    submit = SubmitField('sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken. Please choose a different one.')



'''
This class is for Login
Here we have Email,Password,and submit button
We have applied Some Validators as well from the above Modules E.g wtform.validators
'''

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class UpdateAccountForm(FlaskForm):
    username = StringField('username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',
                        validators=[DataRequired(),Email()])


    picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')


    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Post')



class CommentForm(FlaskForm):
    content = TextField('Comments')
    submit = SubmitField('Comment')

class MovieSearchForm(FlaskForm):

    choices = [('Movie', 'Movie'),('TV', 'TV'),('Actor', 'Actor')]
    select = SelectField('Search for:', choices=choices)
    search_movies = StringField('Search',validators=[DataRequired(),Length(min=2,max=150)],render_kw={"placeholder": "Search movies,tv,actors and more...."})
    submit = SubmitField('Search')




class Favourite_form(FlaskForm):
    Fav = SubmitField('Add To Favourite')



class SearchForm(FlaskForm):
    autocomp = TextField('Insert City', id='myInput')



class CompareForm(FlaskForm):
    movie_1 = IntegerField("movie_id",validators = [NumberRange])
    movie_2 = IntegerField("movie_id",validators = [NumberRange])
    submit = SubmitField('Compare')



class NewsForm(FlaskForm):
    search_new = StringField('Get Updates')
    submit = SubmitField('Find')