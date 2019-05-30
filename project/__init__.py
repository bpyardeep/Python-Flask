from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

'''
This SECRET_KEY will protect the Modification of any Cookie and CyberAttacks
'''


app.config['SECRET_KEY'] = '3dcd5811e8ab589bda5a206d3e24193d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
# engine = create_engine('sqlite:///site.db', echo=True)
# Session = sessionmaker(bind=engine)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'



from project import routes
