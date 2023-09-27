from typing import List
from fastapi import Depends, Response, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2, utils
from ..database import get_db

router = APIRouter(
    prefix='/users'
)

########################### 👤 ADD NEW USER [ CREATE ] ✅ ###########################
# This route allows the creation of a new user by handling POST requests.
# It expects user data as input and returns the newly created user data.
# If successful, it responds with a status code 201 (Created).
@router.post("/", response_model=schemas.UserResponseData, status_code=status.HTTP_201_CREATED)
def add_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the user's password for security.
    hash_password = utils.get_password_hash(user_data.password)
    user_data.password = hash_password

    # Create a new user instance using the input data.
    new_user = models.User(**user_data.model_dump())

    # Add the new user to the database, commit the transaction, and refresh to get the updated user data.
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return the newly created user data.
    return new_user


########################### 👤 GET ALL USER [ READ ] ###########################
# This route allows fetching a list of all users from the database by handling GET requests.
# It retrieves all user records from the database and returns them as a list of user data.
@router.get("/", response_model=List[schemas.UserResponseData])
def all_users(db: Session = Depends(get_db)):

    # Query the database to retrieve all user records.
    users = db.query(models.User).all()

    # Return the list of user data.
    return users
