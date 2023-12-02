# FLASK LIST TO DO APP
Overview
This project is a Flask-based web application that utilizes SQLAlchemy as its ORM (Object-Relational Mapping) for database interactions. The application models include User, Tweet, and Following to implement a basic social media platform. The project structure is organized into three main files: pipfile, db.py, and model files (user_model.py, task_model.py, user.py, task.py).

## Getting Started
### Prerequisites
- Python 3.12
- PostgreSQL database (You can use the provided .env file for the connection details)

## Dependencies
The project utilizes the following Python packages:

```python
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
flask = "*"
flask-sqlalchemy = "*"
psycopg2-binary = "*"
bcrypt = "*"
flask-bcrypt = "*"
marshmallow = "*"
injector = "*"
pyjwt = "*"

[dev-packages]

[requires]
python_version = "3.12"
```
### Installation
1. Clone the repository:
```bash
git clone https://github.com/RevoU-FSSE-2/Week-22-Hill-Man-1.git
```
### Install dependencies:
```bash
pip install -r requirements.txt
```
2. Set up the database:
Uncomment the following lines in app.py to initialize the database:

``` python
# with app.app_context():
#     db_init()
```

### Create and populate the .env file:
Create a file named .env in the project root and add the following:

```env
DATABASE_URL=postgresql://postgres:RevouWeek21***@db.dxtvuacfifnhoufyzvca.supabase.co:5432/postgres
SECRET_KEY=thisis*****
```
Replace placeholders with your actual database connection details.

## Running the App
Run the Flask application with the following command:

```bash
python app.py
```
The app will be accessible at http://localhost:5000.
## API Endpoints

### User Routes

- **POST /auth/login**: Logs in a user and returns a JWT token.
- **GET /auth/users**: Fetches all users (Admin access only).
- **PUT /auth/:id**: Updates user data by id (Admin access only).
- **GET /auth/:id**: Gets user data by id (Admin access only).
- **DELETE /auth/:id**: Deletes a user by id (Admin access only).

### Task Routes

- **POST /task/create** : Creates a new task for a user.
- **PUT /task/:id** : Updates a task by id.
- **GET /task/:id** : Gets a task by id.
- **GET /task/** : Gets all tasks for a user.

### Admin Routes

- **GET /admin/users** : Fetches all users.
- **PUT /admin/:id** : Updates user data by id.
- **GET /admin/:id** : Gets user data by id.
- **DELETE /admin/:id** : Deletes a user by id.

## Technology Stack

- **Backend** : Node.js, Express
- **Database** : MongoDB
- **Authentication** : JWT Tokens
- **Middleware** : cors, cookie-parser, helmet, multer

## Contributing
Contributions are welcome! If you find a bug or want to add a new feature, please create an issue or a pull request.

## POSTMAN LINK
**https://www.postman.com/research-cosmonaut-88926417/workspace/w21/collection/29017942-f4453d55-55e9-414f-904a-3df4fedaf88e**

## FE REPO
**https://github.com/Hill-Man-1/week-22-fe**

## Author
Hilman Syarifudin
