from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth_utils import decode_access_token
from app.models import User
from app.database import get_db

# Create an OAuth2 scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Decode the access token to get the user's email
    email = decode_access_token(token)
    if email is None:
        # Raise an exception if the token is invalid
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Query the database to find the user with the given email
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        # Raise an exception if the user is not found in the database
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return the user object if found
    return user
