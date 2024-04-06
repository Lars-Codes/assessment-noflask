# assessment

# Coding assessment 

### Stack
  - Python 
  - Flask 
  - MySQL
  - HTML
  - CSS
  - JavaScript (vanilla) 

## Table of Contents

- [Project Name](#project-name)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)


## Getting Started

### Prerequisites 
You must have MySQL installed on your machine. Installation instructions can be found [here]([URL](https://www.mysql.com/)).


3. **Create a Users Collection**:

To store data for this application, you'll need to create a database to store vehicle data. 

In the server directory, create a .env file with the following data: 

```plaintext
FLASK_ENV=development
FLASK_APP=app.py
FLASK_RUN_PORT=8000
SQLALCHEMY_DATABASE_URI=mysql+pymysql://username:password@localhost:3306/database_name
BASE_URL=http://localhost:8000
```
You may need to adjust the port depending on where MySQL is running on your machine. Update username, password, and database_name 
with your credentials. 

5. **Start the Development Server**:
```bash
# Navigate to the project directory
cd server

# install dependencies 
pip install -r requirements.txt

# Run the development server 
flask run 
```

Now, open your browser and follow the link displayed on the frontend server to run the application. Click the query button to 
make a query and the insert button to make an insertion to test the code. Also specify if you would like your data to be 
processed and returned in big or little endian format. If none is detected, it will default to big endian. 




