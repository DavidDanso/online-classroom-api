from typing import List
from fastapi import Depends, Response, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/my-courses'
)

########################### 🔵 STUDENT ENROLLED COURSES [ READ ] ###########################
# Define a GET route to retrieve a list of student enrolled courses
@router.get("/", response_model=List[schemas.StudentEnrolledCourseResponseData])
def all_enrollments(db: Session = Depends(get_db), 
                    current_user: dict = Depends(oauth2.get_current_user)):

    # Query the database to retrieve all enrollments for the current user
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.student_fkey == current_user.user_id).all()
    
    # Return the list of enrollments as a response
    return enrollment


########################### 🔵 STUDENT ENROLLED COURSES ENROLLMENT BY ID [ READ ] ###########################
# This endpoint allows retrieval of enrollment details for a specific course by its ID.
@router.get("/{enrollment_id}", response_model=schemas.EnrollmentResponseData)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db), 
                    current_user: dict = Depends(oauth2.get_current_user)):

    # Query the database to find the enrollment record with the given ID.
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.enrollment_id == enrollment_id).first()

    # Check if the enrollment record exists.
    if enrollment is None:
        # If the enrollment record is not found, raise a 403 Forbidden HTTP error.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Course Enrollment with ID: {enrollment_id} is not found")
    
    # Check if the current user is the owner of this enrollment.
    if current_user.user_id != enrollment.student_info.user_id:
        # If the current user is not the owner, raise a 403 Forbidden error.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Your view of courses is limited to those that you have enrolled in")
    
    # If all checks pass, return the enrollment details.
    return enrollment


########################### 🔵 DELETE COURSE ENROLLMENT BY ID [ DELETE ] ❌ ###########################
@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course_enrollment(enrollment_id: int, db: Session = Depends(get_db), 
                    current_user: dict = Depends(oauth2.get_current_user)):

    # Create a query to retrieve the course enrollment with the specified ID from the database
    enrollment_query = db.query(models.Enrollment).filter(models.Enrollment.enrollment_id == enrollment_id)
    
    # Fetch the enrollment record from the database
    enrollment = enrollment_query.first()

    # Check if the enrollment record exists; if not, raise a 403 Forbidden error
    if enrollment is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Course Enrollment with ID: {enrollment_id} is not found")
    
    # Verify if the user attempting to delete the enrollment is the owner of the enrollment
    if current_user.user_id != enrollment.student_info.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="You don't have permission to delete this enrollment data")
    
    # Delete the enrollment record from the database (synchronize_session=False for better performance)
    enrollment_query.delete(synchronize_session=False)
    
    # Commit the changes to the database
    db.commit()
    
    # Return a response indicating a successful deletion with a status code 204 (No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
