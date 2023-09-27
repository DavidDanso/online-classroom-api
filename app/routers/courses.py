from typing import List
from fastapi import Depends, Response, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/courses'
)

########################### 📒 CREATE A NEW COURSE [ CREATE ] ✅ ###########################
# Define a route for creating a new course using HTTP POST method.
@router.post("/", response_model=schemas.CourseResponseData, status_code=status.HTTP_201_CREATED)
def add_course(course_data: schemas.CourseCreate, db: Session = Depends(get_db), 
               current_user: dict = Depends(oauth2.get_current_user)):
    
    # Retrieve a list of existing course names from the database.
    courses = [course.course_name for course in db.query(models.Course).all()]
    
    # Check if the provided course name already exists in the list of courses.
    if course_data.course_name in courses:
        # If it exists, raise a Forbidden HTTPException with a message indicating duplication.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"{course_data.course_name} is already added")
    
    # Check if the current user has the 'lecturer' role, allowing them to add a new course.
    if current_user.role == 'lecturer':
        # Create a new course instance with the provided data and the user's ID as the owner.
        new_course = models.Course(user_role=current_user.user_id, **course_data.model_dump())
        # Add the new course to the database session.
        db.add(new_course)
        # Commit the changes to the database.
        db.commit()
        # Refresh the new_course object to ensure it reflects the database state.
        db.refresh(new_course)

    else:
        # If the current user does not have the 'lecturer' role, raise a Forbidden HTTPException.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Only lecturers are allowed to add new courses")

    # Return the newly created course as a response.
    return new_course


########################### 📒 GET LIST OF ALL COURSES [ READ ] ###########################
@router.get("/", response_model=List[schemas.CourseResponseData])
# Define a GET route to retrieve a list of all courses
def all_courses(db: Session = Depends(get_db)):
    # Query the database to retrieve all courses
    courses = db.query(models.Course).all()

    # Return the list of courses as a response
    return courses


########################### 📒 GET DETAILS OF A SPECIFIC COURSE [ READ ] ###########################
# Define an API endpoint to retrieve details of a specific course.
# The endpoint takes the 'course_id' as a parameter to identify the course.
# The 'response_model' is specified to ensure the response follows the defined data schema.
@router.get("/{course_id}", response_model=schemas.CourseResponseData)
def get_course(course_id: int, db: Session = Depends(get_db)):
    
    # Query the database to retrieve the course with the provided 'course_id'.
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()

    # Check if the course exists in the database. If not, raise an HTTP exception.
    if course is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Course with ID: {course_id} not found")

    # Return the details of the course as the response.
    return course


########################### 📒 UPDATE AN EXISTING COURSE [ UPDATE ] ###########################
@router.put("/{course_id}", response_model=schemas.CourseResponseData)
def update_course(course_id: int, course_data: schemas.CourseUpdate, db: Session = Depends(get_db), 
                  current_user: dict = Depends(oauth2.get_current_user)):
    
    # Query the database to find the course with the specified course_id
    course_query = db.query(models.Course).filter(models.Course.course_id == course_id)
    course = course_query.first()

    # Check if the course with the given ID exists
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Course with ID: {course_id} not found")
    
    # Check if the current user has permission to update this course
    if current_user.user_id != course.user_role and current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"You don't have permission to update this course")
    
    # Update the course data with the provided changes (excluding unset fields)
    course_query.update(course_data.model_dump(exclude_unset=True), synchronize_session=False)

    # Commit the changes to the database
    db.commit()

    # Refresh the course object to reflect the updated data
    db.refresh(course_query.first())

    # Return the updated course data
    return course_query.first()


########################### 📒 DELETE A COURSE [ DELETE ] ❌ ###########################
# This endpoint handles the deletion of a course based on its unique course_id.
@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db), 
                  current_user: dict = Depends(oauth2.get_current_user)):
    # Query the database to find the course with the specified course_id.
    course_query = db.query(models.Course).filter(models.Course.course_id == course_id)
    course = course_query.first()

    # If the course is not found, raise a 403 Forbidden HTTP exception.
    if course is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Course with ID: {course_id} not found")
    
    # Check if the current user has the permission to delete the course.
    # Users can delete their own courses, and admin users have permission as well.
    if current_user.user_id != course.user_role and current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"You don't have permission to delete this course")
    
    # Delete the course from the database without synchronizing the session.
    course_query.delete(synchronize_session=False)
    db.commit()

    # Return a successful response with a status code of 204 (No Content) to indicate successful deletion.
    return Response(status_code=status.HTTP_204_NO_CONTENT)



########################### ENROLL IN A COURSE ###########################
# 🔵🔵🔵🔵🔵🔵🔵
########################### ENROLL IN A COURSE ###########################
########################### 🔵 ENROLL IN A COURSE [ CREATE ] ✅ ###########################
@router.post("/{course_id}/enroll", response_model=schemas.EnrollmentResponseData)
def course_enrollment(course_id: int, db: Session = Depends(get_db), 
                      current_user: dict = Depends(oauth2.get_current_user)):

    # Check if the course exists in the database
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if not course:
        # If the course is not found, raise an HTTP exception with a 403 status code and a relevant error message
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Course with ID: {course_id} is not found"
        )

    # Check if the user is already enrolled in this course
    enrolled_courses = [enrollment.course_info.course_name for enrollment in db.query(models.Enrollment).filter(models.Enrollment.student_fkey == current_user.user_id).all()]
    if course.course_name in enrolled_courses:
        # If the user is already enrolled in the course, raise an HTTP exception with a 403 status code and a relevant error message
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You've already enrolled in this course."
        )

    # Create a new enrollment record for the user and the selected course
    enrollment = models.Enrollment(
        student_fkey=current_user.user_id,
        course_fkey=course_id,
    )

    # Add the new enrollment record to the database, commit the transaction, and refresh the enrollment object
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    # Return the newly created enrollment record as a response
    return enrollment



########################### CREATE a NEW LESSON IN a COURSE ###########################
# ⚛️⚛️⚛️⚛️⚛️⚛️
########################### CREATE a NEW LESSON IN a COURSE ###########################

########################### ⚛️ CREATE a NEW LESSON IN a COURSE [ CREATE ] ✅ ###########################
# This endpoint handles the creation of a new lesson within a course.
@router.post("/{course_id}/lessons", response_model=schemas.LessonResponseData)
def add_lesson(course_id: int, lesson_data: schemas.LessonCreate, db: Session = Depends(get_db), 
                      current_user: dict = Depends(oauth2.get_current_user)):
    
    # Check if the specified course exists in the database.
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()

    if not course:
        # If the course is not found, raise an HTTP 403 Forbidden error.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Course with ID: {course_id} is not found"
        )

    # Define roles that are allowed to create lessons (lecturer and admin).
    allowed_roles = ["lecturer", "admin"]
    
    # Check if the current user has the necessary role and permissions to add lessons to the course.
    if current_user.role not in allowed_roles or course.lecturer_info.username != current_user.username:
        # If not, raise an HTTP 403 Forbidden error.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have permission to add new lessons to: [ {course.course_name} ] "
        )
    
    # Retrieve existing lesson titles and contents from the database.
    lesson_titles = [lesson.lesson_title for lesson in db.query(models.Lesson).all()]
    lesson_contents = [lesson.lesson_content for lesson in db.query(models.Lesson).all()]

    # Check if the submitted lesson title already exists in the database.
    if lesson_data.lesson_title in lesson_titles:
        # If it exists, raise an HTTP 403 Forbidden error.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You already have a lesson titled [ {lesson_data.lesson_title} ] "
    )

    # Check if the submitted lesson content already exists in the course.
    if lesson_data.lesson_content in lesson_contents:
        # If it exists, raise an HTTP 403 Forbidden error.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You've already added this lesson data content to {course.course_name} Course"
    )
    
    # Create a new lesson object and add it to the database.
    lesson = models.Lesson(
        user_fkey=current_user.user_id, 
        course_fkey=course_id, 
        **lesson_data.model_dump()
    )
    db.add(lesson)
    db.commit()
    db.refresh(lesson)

    # Return the created lesson as a response.
    return lesson


########################### ⚛️ GET LIST OF ALL LESSONS IN A COURSE [ READ ] ###########################
# Define an endpoint to retrieve a list of all lessons for a given course.
@router.get("/{course_id}/lessons", response_model=List[schemas.LessonResponseData])
def get_lessons(course_id: int, db: Session = Depends(get_db)):
    
    # Query the database to retrieve all lessons associated with the specified course_id.
    lessons = db.query(models.Lesson).filter(models.Lesson.course_fkey == course_id).all()

    # Check if there are no lessons found for the course, and if so, raise a 404 error.
    if not lessons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"This course doesn't have a lesson yet"
        )
    
    # Return the list of lessons as a response.
    return lessons


########################### ⚛️ GET DETAILS OF A SPECIFIC LESSON [ READ ] ###########################
# Define a route that handles HTTP GET requests to retrieve details of a specific lesson.
# It expects the course_id and lesson_id as path parameters.
# The response will be in the format specified by the LessonResponseData schema.
@router.get("/{course_id}/lessons/{lesson_id}", response_model=schemas.LessonResponseData)
def get_lesson(course_id: int, lesson_id: int, db: Session = Depends(get_db)):
    
    # Query the database to retrieve the lesson information based on the provided course_id and lesson_id.
    lesson = db.query(models.Lesson).filter(
        (models.Lesson.course_fkey == course_id) & (models.Lesson.lesson_id == lesson_id)
    ).first()
    
    # If the lesson is not found, raise an HTTPException with a 404 Not Found status code and a relevant detail message.
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson not found"
        )

    # If the lesson is found, return it as a response.
    return lesson


########################### ⚛️ UPDATE AN EXITING LESSON [ PUT ] ###########################
# Define a route for updating a lesson using HTTP PUT method
# The response model is specified as LessonResponseData
@router.put("/{course_id}/lessons/{lesson_id}", response_model=schemas.LessonResponseData)
def update_lesson(
    course_id: int, lesson_id: int, lesson_update: schemas.LessonUpdate,
    db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)
):
    # Retrieve the course associated with the given course_id from the database
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    
    # Query the database for the lesson using the provided lesson_id
    lesson_query = db.query(models.Lesson).filter(models.Lesson.lesson_id == lesson_id)
    
    # Retrieve the lesson object from the query
    lesson = lesson_query.first()
    
    # Check if the course exists, and if not, raise a 404 error
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID: {course_id} not found"
        )
    
    # Check if the lesson exists, and if not, raise a 404 error
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson not found"
        )
    
    # Define a list of allowed roles for updating lessons (e.g., lecturer or admin)
    allowed_roles = ["lecturer", "admin"]
    
    # Check if the current user's role is in the list of allowed roles
    # Also, ensure that the current user is the owner of the lesson
    if current_user.role not in allowed_roles or lesson.user_fkey != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have permission to update this lesson"
        )
    
    # Update the lesson in the database with the provided lesson_update data
    # Exclude unset attributes to prevent overwriting with None values
    lesson_query.update(lesson_update.model_dump(exclude_unset=True), synchronize_session=False)
    
    # Commit the changes to the database
    db.commit()
    
    # Refresh the lesson object to reflect the updated data
    db.refresh(lesson)

    # Return the updated lesson as the response
    return lesson


########################### ⚛️ DELETE A LESSON [ DELETE ] ❌ ###########################
# This is an API route that handles the deletion of a lesson within a specific course.
@router.delete("/{course_id}/lessons/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lesson(course_id: int, lesson_id: int, db: Session = Depends(get_db), 
                  current_user: dict = Depends(oauth2.get_current_user)):

    # Fetch the course associated with the provided 'course_id'.
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()

    # Query the database to find the lesson with the provided 'lesson_id'.
    lesson_query = db.query(models.Lesson).filter(models.Lesson.lesson_id == lesson_id)
    lesson = lesson_query.first()

    # If the course is not found, raise an HTTP 404 Not Found error.
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID: {course_id} not found"
        )
    
    # If the lesson is not found, raise an HTTP 404 Not Found error.
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson not found"
        )
    
    # Define the roles that are allowed to delete lessons (lecturer and admin).
    allowed_roles = ["lecturer", "admin"]

    # Check if the current user's role and ownership match the allowed roles or if they have permission to delete the lesson.
    if current_user.role not in allowed_roles or lesson.user_fkey != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have permission to delete this lesson"
        )

    # Delete the lesson from the database (synchronize_session=False means it won't update the session immediately).
    lesson_query.delete(synchronize_session=False)

    # Commit the changes to the database.
    db.commit()

    # Return a successful response with a 204 No Content status code to indicate successful deletion.
    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################### CREATE a NEW Assignment IN a COURSE ###########################
# 📝📝📝📝📝📝📝
########################### CREATE a NEW Assignment IN a COURSE ###########################

########################### 📝 CREATE a NEW Assignment IN a COURSE [ CREATE ] ✅ ###########################
# This route allows the creation of a new assignment within a course.
@router.post("/{course_id}/assignments", response_model=schemas.AssignmentResponseData)
def add_assignment(course_id: int, assignment_data: schemas.AssignmentCreate, db: Session = Depends(get_db), 
                      current_user: dict = Depends(oauth2.get_current_user)):
    
    # Retrieve the course information based on the given course_id.
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()

    # Check if the course exists; if not, raise a 403 Forbidden error.
    if not course:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Course with ID: {course_id} is not found"
        )

    # Define the roles allowed to add assignments (lecturer and admin).
    allowed_roles = ["lecturer", "admin"]
    
    # Check if the current user's role and username match the allowed roles and the course's lecturer.
    if current_user.role not in allowed_roles or course.lecturer_info.username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have permission to add a new assignment to the '{course.course_name}' course"
        )
    
    # Retrieve existing assignment titles and descriptions from the database.
    assignment_titles = [assignment.assignment_title for assignment in db.query(models.Assignment).all()]
    assignment_descriptions = [assignment.assignment_description for assignment in db.query(models.Assignment).all()]

    # Check if an assignment with the same title or description already exists; if so, raise a 403 Forbidden error.
    if assignment_data.assignment_title in assignment_titles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"A Course Assignment with the title '{assignment_data.assignment_title}' already exists"
        )

    if assignment_data.assignment_description in assignment_descriptions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="An assignment with this description has already been added."
        )
    
    # Create a new assignment record and add it to the database.
    assignment = models.Assignment(
        user_fkey=current_user.user_id, 
        course_fkey=course_id, 
        **assignment_data.model_dump()
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    # Return the newly created assignment.
    return assignment


########################### 📝 GET LIST OF ALL ASSIGNMENTS IN A COURSE [ READ ] ###########################
@router.get("/{course_id}/assignments", response_model=List[schemas.AssignmentResponseData])
def get_assignments(course_id: int, db: Session = Depends(get_db), 
                      current_user: dict = Depends(oauth2.get_current_user)):
    # Retrieve the course associated with the given course_id
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()

    # Check if the course exists; if not, raise an HTTPException with a 403 Forbidden status
    if not course:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Course with ID: {course_id} is not found"
        )

    # Retrieve all assignments related to the specified course
    assignments = db.query(models.Assignment).filter(models.Assignment.course_fkey == course_id).all()

    # If no assignments are found, raise an HTTPException with a 404 Not Found status
    if not assignments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assignment not Found"
        )
    
    # Return the list of assignments
    return assignments


########################### 📝 GET DETAILS OF A SPECIFIC ASSIGNMENT [ READ ] ###########################
# This route retrieves details of a specific assignment for a given course.
# It expects a course ID and an assignment ID as parameters.
@router.get("/{course_id}/assignments/{assignment_id}", response_model=schemas.AssignmentResponseData)
def get_lesson(course_id: int, assignment_id: int, db: Session = Depends(get_db)):
    
    # Retrieve the course with the specified course ID from the database.
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()

    # If the course is not found, raise a 404 Not Found error.
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID: {course_id} is not found"
        )
    
    # Retrieve the assignment with the specified assignment ID and associated with the course.
    assignment = db.query(models.Assignment).filter(
        (models.Assignment.course_fkey == course_id) & (models.Assignment.assignment_id == assignment_id)
    ).first()
    
    # If the assignment is not found, raise a 404 Not Found error.
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assignment not found"
        )

    # Return the retrieved assignment data.
    return assignment


########################### 📝 UPDATE AN EXISTING ASSIGNMENT [ PUT ] ###########################
# Define a PUT endpoint to update an existing assignment within a course.
# This endpoint expects the following parameters:
# - course_id: The ID of the course to which the assignment belongs.
# - assignment_id: The ID of the assignment to be updated.
# - assignment_update: The data representing the updated assignment (in the request body).
# - db: The database session dependency.
# - current_user: The current user (authenticated) dependency.

@router.put("/{course_id}/assignments/{assignment_id}", response_model=schemas.AssignmentResponseData)
def update_assignment(course_id: int, assignment_id: int, assignment_update: schemas.AssignmentUpdate, 
               db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    
    # Query the database to retrieve the course associated with the given course_id.
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    
    # Query the database to retrieve the assignment to be updated based on assignment_id.
    assignment_query = db.query(models.Assignment).filter(models.Assignment.assignment_id == assignment_id)
    assignment = assignment_query.first()
    
    # Check if the course exists; if not, raise a 404 error.
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID: {course_id} not found"
        )
    
    # Check if the assignment exists; if not, raise a 404 error.
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assignment not found"
        )
    
    # Define the allowed user roles (lecturer and admin) to update assignments.
    allowed_roles = ["lecturer", "admin"]
    
    # Check if the current user has the necessary role and is the owner of the assignment; if not, raise a 403 error.
    if current_user.role not in allowed_roles or assignment.user_fkey != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have permission to update this assignment"
        )
    
    # Update the assignment in the database with the provided assignment_update data.
    assignment_query.update(assignment_update.model_dump(exclude_unset=True), synchronize_session=False)
    
    # Commit the changes to the database.
    db.commit()
    
    # Refresh the assignment object to reflect the updated data.
    db.refresh(assignment)

    # Return the updated assignment data as a response.
    return assignment


########################### 📝 DELETE ASSIGNMENT [ DELETE ] ❌ ###########################
@router.delete("/{course_id}/assignments/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(course_id: int, assignment_id: int, db: Session = Depends(get_db), 
                  current_user: dict = Depends(oauth2.get_current_user)):
    
    # Query the database to find the course associated with the given course_id
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    
    # Query the database to find the assignment associated with the given assignment_id
    assignment_query = db.query(models.Assignment).filter(models.Assignment.assignment_id == assignment_id)
    assignment = assignment_query.first()

    # If the course does not exist, raise a 404 Not Found error
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID: {course_id} not found"
        )
    
    # If the assignment does not exist, raise a 404 Not Found error
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assignment not found"
        )
    
    # Define the roles that are allowed to delete assignments (lecturer and admin)
    allowed_roles = ["lecturer", "admin"]
    
    # Check if the current user's role and ownership match the allowed roles or if they are the creator of the assignment
    if current_user.role not in allowed_roles or assignment.user_fkey != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have permission to delete this assignment"
        )
    
    # Delete the assignment from the database without synchronizing with the session
    assignment_query.delete(synchronize_session=False)
    
    # Commit the changes to the database
    db.commit()

    # Return a response with a 204 No Content status code to indicate successful deletion
    return Response(status_code=status.HTTP_204_NO_CONTENT)
