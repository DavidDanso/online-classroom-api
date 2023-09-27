# Online-Classroom-API

This API offers endpoints for handling, organizing, and viewing educational course data

## Frameworks and Tools

The API was built using the following frameworks and tools:

- [FastAPI](https://fastapi.tiangolo.com/): A modern, fast, web framework for building APIs with Python 3.7+ based on standard Python type hints.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/): A database migration tool for SQLAlchemy, allowing you to manage changes to your database schema over time.
- [PostgreSQL](https://www.postgresql.org/): A powerful, open-source relational database management system.
- [SQLAlchemy](https://www.sqlalchemy.org/): A SQL toolkit and Object-Relational Mapping (ORM) library for Python.

## Endpoints

### 1) Create a Course

**Method:** POST
**Endpoint:** `/courses`
**Description:** Create a new course.

### 2) Update Course

**Method:** PUT
**Endpoint:** `/courses/{course_id}`
**Description:** Update an existing course.

### 3) View Courses

**Method:** GET
**Endpoint:** `/courses`
**Description:** View a list of all courses.

### 3.1) View a Course

**Method:** GET
**Endpoint:** `/courses/{course_id}`
**Description:** View details of a specific course.

### 4) Cancel Appointment

**Method:** DELETE
**Endpoint:** `/courses/{course_id}`
**Description:** Cancel an existing course.

### 5) User Registration

**Method:** POST
**Endpoint:** `/users`
**Description:** Register a new user account.

### 6) User Login

**Method:** POST
**Endpoint:** `/login`
**Description:** Log in and receive an access token for API interactions.

### 7) Enroll in a Course

**Method:** POST
**Endpoint:** `/courses/{course_id}/enroll`
**Description:** Enroll in a course.

### 8) Create a Lesson

**Method:** POST
**Endpoint:** `/courses/{course_id}/lessons`
**Description:** Create a new lesson within a course.

### 9) View Lessons

**Method:** GET
**Endpoint:** `/courses/{course_id}/lessons`
**Description:** View all lessons within a course.

### 10) View a Lesson

**Method:** GET
**Endpoint:** `/courses/{course_id}/lessons/{lesson_id}`
**Description:** View details of a specific lesson.

### 11) Update a Lesson

**Method:** PUT
**Endpoint:** `/courses/{course_id}/lessons/{lesson_id}`
**Description:** Update a lesson.

### 12) Delete a Lesson

**Method:** DELETE
**Endpoint:** `/courses/{course_id}/lessons/{lesson_id}`
**Description:** Delete a lesson.

### 13) Create an Assignment

**Method:** POST
**Endpoint:** `/courses/{course_id}/assignments`
**Description:** Create a new assignment within a course.

### 14) View Assignments

**Method:** GET
**Endpoint:** `/courses/{course_id}/assignments`
**Description:** View all assignments within a course.

### 15) View an Assignment

**Method:** GET
**Endpoint:** `/courses/{course_id}/assignments/{assignment_id}`
**Description:** View details of a specific assignment.

### 16) Update an Assignment

**Method:** PUT
**Endpoint:** `/courses/{course_id}/assignments/{assignment_id}`
**Description:** Update an assignment.

### 17) Delete an Assignment

**Method:** DELETE
**Endpoint:** `/courses/{course_id}/assignments/{assignment_id}`
**Description:** Delete an assignment.

## How to Run Locally

1. Clone this repository:
   
```
git clone https://github.com/DavidDanso/online-classroom-api.git
```

```
cd online-classroom-api
```


2. Set up a virtual environment to isolate project dependencies:

On Windows
```
python -m venv venv
```

On macOS and Linux
```
python3 -m venv venv
```

2.1. Activate the virtual environment:

On Windows
```
venv\Scripts\activate
```

On macOS and Linux
```
source venv/bin/activate
```


3. Install FastAPI with all dependencies or install all the packages in the requirements.txt file:

```
pip3 install fastapi[all]
```

```
pip3 install -r requirements.txt
```


4. Run the API using uvicorn:

```
uvicorn app.main:app --reload
```


5. Access the API documentation by visiting the following URL in your browser:

```
http://127.0.0.1:8000/docs
```


## Setting Up Database

1. Create a PostgreSQL database.
2. Create a file named .env in the project directory and add the following configuration:

```
DATABASE_HOSTNAME = localhost
DATABASE_PORT = 5432
DATABASE_PASSWORD = your_database_password
DATABASE_NAME = your_database_name
DATABASE_USERNAME = your_database_username
SECRET_KEY = your_secret_key
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60
```

Replace your_database_password, your_database_name, your_database_username, and your_secret_key with appropriate values.

## YouTube Learning Resource

You can learn more about FastAPI by watching the tutorial series on YouTube:

[FastAPI Tutorial Playlist](https://www.youtube.com/watch?v=Yw4LmMQXXFs&list=PL8VzFQ8k4U1L5QpSapVEzoSfob-4CR8zM&index=2)

DavidDanso - davidkellybrownson@gmail.com


