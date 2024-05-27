from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Users
from database import SessionLocal
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext
from logs.app_logger import get_logger
logger = get_logger(__name__)

router = APIRouter(
    prefix='/user',
    tags=['user']
)

# Function to access the database
def get_db():
    logger.info("Created an local instance of the database")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Used to verify the current and changed password for the authenticated user
class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=4)

# We get the user information for the authenticated user
@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    logger.info(f"Getting the information for the user: {user.get('id')}")
    if user is None:
        logger.info(f"Non-authenticated access")
        raise HTTPException(status_code=401, details='Authentication Failed')
    
    logger.info(f"Successfully retrieved the information for the user: {user.get('id')}")
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency,
                          user_verification: UserVerification):
    logger.info(f"Request by user: {user.get('id')}")
    if user is None:
        logger.info(f"Non-authenticated access")
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        logger.warning("Authentication failed, failed to change the password")
        raise HTTPException(status_code=401, detail='Error on the password change')
    
    logger.info(f"Successfully changed the password for user: {user_model.id}")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()