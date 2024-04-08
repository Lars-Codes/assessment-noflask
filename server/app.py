import threading
from concurrent.futures import ThreadPoolExecutor

# configuration 
from flask import Flask 
# handles SQLAlchemy database migrations for Flask migrations using ALembic (database migration tool).
from flask_migrate import Migrate
import os 
# import db from models. 
from models.db import db 
# import vehicle for proper table creation
from models.vehicle import Vehicle
from dotenv import load_dotenv

app = Flask(__name__)
app.config.from_object(__name__) # used to load configuration variables defined in pythn files 

# Import socket utils after declaring app to avoid circular import errors 
from networking.socket_utils import SocketUtils


# load config variables from .env file for mySQL 
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') # load database URI from .env file
# Disable SQLAlchemy modification tracking. Introduces overhead and 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.config['DEBUG'] = True  # Enable debug mode

db.init_app(app)

# used for database migrations 
migrate = Migrate(app, db)

# Start the server
server_address = ('localhost', 10000)

# Create socket from the server address
sock = SocketUtils.create_socket(server_address)

workers = 100
executor = ThreadPoolExecutor(max_workers=workers) # can handle 100 concurrent connections

def handle_client(connection):
    try:
        with(app.app_context()):
            while True:
                data = SocketUtils.receive_data(connection)
                if data:
                    SocketUtils.send_data(connection, data)
                else:
                    break
    finally:
        SocketUtils.close_connection(connection)

def accept_clients():
    try:
        while True:
            connection, client_address = SocketUtils.accept_connection(sock)
            executor.submit(handle_client, connection)
    except Exception as e:
        print(f"Error accepting clients: {e}")

accept_thread = threading.Thread(target=accept_clients)
accept_thread.start()
