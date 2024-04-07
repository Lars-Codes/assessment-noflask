# assessment

# Coding assessment 

### Stack
  - Python 
  - Flask 
  - MySQL
  - HTML
  - CSS
  - JavaScript (vanilla) 

## Getting Started

### Quick explanation 
There are three main files for the application: 
1. server/api/vehicle.py (API)
2. server/service/processing.py (Processing layer)
3. server/models/vehicle.py (Database handling) 

server/api/vehicle.py is the file that retrieves data from the client applications. The query() function handles queries, and the insert() function handles inserts. Both functions route the data to server/service/processing.py. 

server/service/processing.py is responsible for encoding/decoding requests/responses and returning it to the API or sending it to the model for database insertion. 

server/models/vehicle.py is responsible for database handling. 

### Prerequisites 
You must have MySQL installed on your machine. Installation instructions can be found [here](https://www.mysql.com/).


3. **Create Database**:

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

5. **Start the Development Server**:
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

Now, open your browser and follow the link displayed on the frontend server to run the application. Click the query button to 
make a query and the insert button to make an insertion to test the code. Also specify if you would like your data to be 
processed and returned in big or little endian format. If none is detected, it will default to big endian. 




