from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from . import models, schemas
from sqlalchemy.orm import Session
from .database import get_db
from .config import app_settings


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = {app_settings.SECRET_KEY}
ALGORITHM = {app_settings.ALGORITHM}
ACCESS_TOKEN_EXPIRE_MINUTES = {app_settings.ACCESS_TOKEN_EXPIRE_MINUTES}

# Create an instance of the OAuth2PasswordBearer class.
# This instance will be used to authenticate users based on OAuth2 tokens.
# The "tokenUrl" parameter specifies the URL where clients can request tokens (e.g., during login).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Function to create an access token by encoding a payload with an expiration time.
def create_access_token(data: dict):
    # Create a copy of the data to encode.
    to_encode = data.copy()
    
    # Calculate the token's expiration time.
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add the expiration time to the payload.
    to_encode.update({"exp": expire})
    
    # Encode the payload into a JSON Web Token (JWT) using the secret key and algorithm.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # Return the encoded JWT as the access token.
    return encoded_jwt

# Function to verify the access token's validity and extract user data.
def verify_access_token(token: str, credentials_exception):
    try:
        # Decode the access token using the secret key and algorithm.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract the username from the payload.
        username: str = payload.get("username")
        
        # If the username is not present in the payload, raise a credentials exception.
        if username is None:
            raise credentials_exception
        
        # Create a TokenData object containing the extracted username.
        token_data = schemas.TokenData(username=username)
    except JWTError:
        # If there's a JWTError, raise a credentials exception.
        raise credentials_exception
    
    # Return the extracted token data.
    return token_data

# Function to retrieve the current user based on the access token.
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Create an exception for handling credentials-related issues.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify the access token and extract token data.
    token = verify_access_token(token, credentials_exception)
    
    # Query the database to retrieve the user associated with the extracted username.
    user = db.query(models.User).filter(models.User.username == token.username).first()
    
    # Return the user object as the current user.
    return user
