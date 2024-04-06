# configuration 
from flask import Flask 

# handles SQLAlchemy database migrations for Flask migrations using ALembic (database migration tool).
from flask_migrate import Migrate
import os 

# import db from models. 
from models.db import db 
# import vehicle for proper table creation
from models.vehicle import Vehicle

#import blueprint for vehicle
from api.vehicle import vehicle_bp

from dotenv import load_dotenv

app = Flask(__name__, template_folder='templates')
app.config.from_object(__name__) # used to load configuration variables defined in pythn files 

# register blueprint with app 
app.register_blueprint(vehicle_bp)

# load config variables from .env file for mySQL 
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') # load database URI from .env file
# Disable SQLAlchemy modification tracking. Introduces overhead and 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.config['DEBUG'] = True  # Enable debug mode


db.init_app(app)

# used for database migrations 
migrate = Migrate(app, db)
