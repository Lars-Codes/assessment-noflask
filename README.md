# assessment

# Coding assessment 

### Stack
  - Python 
  - Flask 
  - MySQL

## Getting Started

### Quick explanation 
There are three main files for the application: 
1. server/networking/socket_utils.py (Socket utilities)
2. server/service/processing.py (Processing layer)
3. server/models/vehicle.py (Database handling) 

server/networking/socket_utils.py is the file that retrieves data from the client applications and sends a response back.
server/service/processing.py is responsible for encoding/decoding requests/responses and returning it to the API or sending it to the model for database insertion. 

server/models/vehicle.py is responsible for database handling. 

### Prerequisites 
You must have MySQL installed on your machine. Installation instructions can be found [here](https://www.mysql.com/).

**Create Database**:

To store data for this application, you'll need to create a database to store vehicle data. 

In the server directory, create a .env file with the following data: 

```plaintext
FLASK_ENV=development
FLASK_APP=app.py
FLASK_RUN_PORT=8000
SQLALCHEMY_DATABASE_URI=mysql+pymysql://username:password@localhost:3306/database_name
```
You may need to adjust the port depending on where MySQL is running on your machine. Update username, password, and database_name 
with your credentials. 

**Start the Development Server**:
```bash
# Navigate to the project directory
cd server

# install dependencies 
pip install -r requirements.txt

# Initialize database table
flask db init
flask db migrate
flask db upgrade 

# Run the development server 
flask run 
```
**Test using client**:
Use the dummy app.py file to send data to this server application. Comment/uncomment provided dummy data in the try/catch block to send/retrieve data. 




# assessment-noflask
