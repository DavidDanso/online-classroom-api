from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import asc

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix='/assignments'
)

###########################  📝 GET ALL ASSIGNMENTS [ READ ] ###########################
# Define a route to handle HTTP GET requests for retrieving all assignments
@router.get("/", response_model=List[schemas.AssignmentResponseData])
def get_assignments(db: Session = Depends(get_db)):
    # Retrieve all assignments from the database
    assignments = db.query(models.Assignment).order_by(asc(models.Assignment.assignment_id)).all()
    
    # Return the list of assignments as a response
    return assignments
