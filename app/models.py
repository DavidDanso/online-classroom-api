from sqlalchemy import ARRAY, TIMESTAMP, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

from .database import Base

# Define a SQLAlchemy model for the 'users' table
class User(Base):
    # Specify the table name in the database
    __tablename__ = "users"

    # Unique identifier for the user
    user_id = Column(Integer, primary_key=True, index=True, nullable=False)

    # User's username (must be unique)
    username = Column(String, unique=True, index=True, nullable=False)

    # User's password (hashed)
    password = Column(String, index=True, nullable=False)

    # User's email address (must be unique)
    email = Column(String, unique=True, index=True, nullable=False)

    # Role of the user (e.g., lecturer, student, admin)
    role = Column(String, nullable=False)

    # Creation timestamp with timezone information, set to the current timestamp by default
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)


# Define a SQLAlchemy model class for the "courses" table.
class Course(Base):
    # Set the table name for this model.
    __tablename__ = "courses"

    # Define columns for the "courses" table.
    course_id = Column(Integer, primary_key=True, index=True, nullable=False)  # Primary key for course records.
    course_name = Column(String, index=True, nullable=False)  # Name of the course.
    course_description = Column(String, nullable=False)  # Description of the course.
    course_instructor = Column(String, nullable=False)  # Instructor's name for the course.
    course_capacity = Column(Integer, nullable=False)  # Maximum capacity of the course.
    course_location = Column(String, nullable=False)  # Location where the course is held.

    start_date = Column(String, nullable=False)  # Start date of the course.
    end_date = Column(String, nullable=False)  # End date of the course.

    # Define a foreign key relationship to the "users" table, indicating the user's role in this course.
    user_role = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    # Define a timestamp for when the course record was created.
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

    # Define a relationship with the "User" model to access information about the course instructor.
    lecturer_info = relationship("User")


# Define an SQLAlchemy model for representing enrollments in a database table.
class Enrollment(Base):
    # Define the name of the database table for this model.
    __tablename__ = "enrollments"

    # Define the primary key column for enrollment records.
    enrollment_id = Column(Integer, primary_key=True, index=True, nullable=False)

    # Define a column to store a message related to the enrollment, with a default value.
    enrollment_message = Column(String, nullable=False, default="Enrollment successful✅🎉")

    # Define a foreign key column to establish a relationship with the "users" table.
    student_fkey = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    # Define a foreign key column to establish a relationship with the "courses" table.
    course_fkey = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)

    # Define relationships between this table and the "User" and "Course" models.
    student_info = relationship("User")
    course_info = relationship("Course")

    # Define a column to store the creation timestamp for each enrollment record.
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)


# Define a class named Lesson that represents lessons within a course.
class Lesson(Base):
    # Set the table name for the database.
    __tablename__ = "lessons"

    # Define attributes for the Lesson class.
    lesson_id = Column(Integer, primary_key=True, index=True, nullable=False)  # Unique lesson identifier.
    lesson_title = Column(String, nullable=False)  # Title of the lesson.
    lesson_content = Column(String, nullable=False)  # Content or materials for the lesson.

    # Define foreign keys to link to related tables (users and courses).
    user_fkey = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    course_fkey = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)

    # Establish a relationship with the Course class.
    course_info = relationship("Course")

    # Store the timestamp when the lesson was created.
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)


# Define a class named Assignment that represents assignments within a course.
class Assignment(Base):
    # Set the table name for the database.
    __tablename__ = "assignments"

    # Define attributes for the Assignment class.
    assignment_id = Column(Integer, primary_key=True, index=True, nullable=False)  # Unique assignment identifier.
    assignment_title = Column(String, nullable=False)  # Title of the assignment.
    assignment_description = Column(String, nullable=False)  # Description of the assignment.
    assignment_questions = Column(ARRAY(String), nullable=False)  # List of assignment questions.
    assignment_instruction = Column(String, nullable=False)  # Instructions for completing the assignment.
    due_date = Column(String, nullable=False)  # Due date for the assignment.
    max_score = Column(Integer, nullable=False)  # Maximum possible score for the assignment.

    # Define foreign keys to link to related tables (users and courses).
    user_fkey = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    course_fkey = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)

    # Establish a relationship with the Course class.
    course_info = relationship("Course")

    # Store the timestamp when the assignment was created.
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)