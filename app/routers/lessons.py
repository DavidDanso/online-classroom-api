from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import asc

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix='/lessons'
)

########################### ⚛️ ALL LESSONS [ READ ] ###########################
# This endpoint is used to retrieve a list of all lessons.
# It responds with a JSON list containing lesson data.
@router.get("/", response_model=List[schemas.LessonResponseData])
def get_lessons(db: Session = Depends(get_db)):

    # Query the database to retrieve all lessons.
    lessons = db.query(models.Lesson).order_by(asc(models.Lesson.lesson_id)).all()

    # Return the list of lessons as the response.
    return lessons
