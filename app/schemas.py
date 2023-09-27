from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

##########################################################👤 USERS SCHEMAS
class UserBase(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    pass

class UserResponseData(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        orm_mode = True


##########################################################👤👤 UserResponseData for LECTURER SCHEMAS
class LecturerResponseData(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
##########################################################👤👤 END UserResponseData for LECTURER SCHEMAS

##########################################################📒 COURSE SCHEMAS
class CourseBase(BaseModel):
    course_name: str
    course_description: str
    course_instructor: str
    course_capacity: int
    course_location: str
    start_date: str
    end_date: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    course_name: Optional[str] = None
    course_description: Optional[str] = None
    course_instructor: Optional[str] = None
    course_capacity: Optional[str] = None
    course_location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class CourseResponseData(CourseBase):
    course_id: int
    created_at: datetime
    lecturer_info: LecturerResponseData

    class Config:
        orm_mode = True


##########################################################🔵 ENROLLMENT ResponseData for LECTURER SCHEMAS
class EnrollStudentResponseData(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class EnrollCourseResponseData(BaseModel):
    course_name: str
    course_description: str
    course_instructor: str
    course_capacity: int
    course_location: str
    start_date: str
    end_date: str
    lecturer_info: LecturerResponseData

    class Config:
        orm_mode = True

class EnrolledResponseData(BaseModel):
    course_name: str
    course_instructor: str
    start_date: str
    end_date: str

    class Config:
        orm_mode = True
##########################################################🔵 END UserResponseData for LECTURER SCHEMAS

##########################################################🔵 ENROLLMENT SCHEMAS
class EnrollmentResponseData(BaseModel):
    enrollment_id: int
    enrollment_message: str

    course_info: EnrollCourseResponseData

    class Config:
        orm_mode = True

class StudentEnrolledCourseResponseData(BaseModel):
    enrollment_id: int
    course_info: EnrolledResponseData

    class Config:
        orm_mode = True


##########################################################⚛️ CourseInfoResponseData for LESSON SCHEMAS
class CourseInfoResponseData(BaseModel):
    course_id: int
    course_name: str
    course_description: str

    class Config:
        orm_mode = True
##########################################################⚛️ END UserResponseData for LESSON SCHEMAS

##########################################################⚛️ LESSON SCHEMAS
class LessonBase(BaseModel):
    lesson_title: str
    lesson_content: str

class LessonCreate(LessonBase):
    pass

class LessonUpdate(BaseModel):
    lesson_title: Optional[str] = None
    lesson_content: Optional[str] = None

class LessonResponseData(BaseModel):
    lesson_id: int
    lesson_title: str
    lesson_content: str
    course_info: CourseInfoResponseData
    created_at: datetime

    class Config:
        orm_mode = True


##########################################################📝📝 ASSIGNMENTS SCHEMAS
class AssignmentBase(BaseModel):
    assignment_title: str
    assignment_description: str
    assignment_questions: List[str]
    assignment_instruction: str
    max_score: int
    due_date: str

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentUpdate(BaseModel):
    assignment_title: Optional[str] = None
    assignment_description: Optional[str] = None
    assignment_questions: Optional[List[str]] = None
    assignment_instruction: Optional[str] = None
    due_date: Optional[str] = None
    max_score: Optional[int] = None

class AssignmentResponseData(BaseModel):
    assignment_id: int
    assignment_title: str
    assignment_description: str
    assignment_questions: List[str]
    assignment_instruction: str
    max_score: int
    due_date: str
    course_info: CourseInfoResponseData
    created_at: datetime

    class Config:
        orm_mode = True

        
################################📜 TOKEN SCHEMAS
# 📜Schemas for authentication tokens

# 📜Represents an authentication token
class Token(BaseModel):
    access_token: str
    token_type: str

# 📜Represents token data for a user
class TokenData(BaseModel):
    username: str | None = None