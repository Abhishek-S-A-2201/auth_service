from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

import os
from dotenv import load_dotenv
load_dotenv()

# Create a password context for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Generate a hash for a given password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token
    :param data: Payload data for the token
    :param expires_delta: Optional expiration time delta
    :return: Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv(
        "JWT_SECRET_KEY"), algorithm=os.getenv(
        "ALGORITHM"))
    return encoded_jwt

def decode_access_token(token: str):
    """
    Decode and verify a JWT access token
    :param token: JWT token to decode
    :return: Email from the token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, os.getenv(
            "JWT_SECRET_KEY"), algorithms=[os.getenv(
                "ALGORITHM")])
        email: str = payload.get("sub")
        if not email:
            raise JWTError
        return email
    except JWTError:
        return None
