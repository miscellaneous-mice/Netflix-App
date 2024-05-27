from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
from pydantic import BaseModel, Field
from models import Users
from passlib.context import CryptContext
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime
from logs.app_logger import get_logger
logger = get_logger(__name__)

# All the requests will be prependded with /auth/
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# Secret key and algorithm used in JWT tokens
SECRET_KEY = 'eFggLaMqVRHG6mOPc3cqa1mlRW2P3A1e'
ALGORITHM = 'HS256'

# Configuration used for hashing passwords
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Used to authenticate every request used to access todo database for their respective databases
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token',
                                    scheme_name="user_oauth2_schema")

# Used for data validation of users
class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    age: int
    password: str
    country: str

# Used for Data validation of our token as to which format our json format of token should be like
class Token(BaseModel):
    access_token: str
    token_type: str

# Function to access the database and retreive database
def get_db():
    db = SessionLocal()
    logger.info("Starting a local database session")
    try:
        yield db # Get's the database to work on
    finally:
        db.close() # After using the database, it is closed

# We assign the local seesion of the db to our db_dependency
db_dependency = Annotated[Session, Depends(get_db)]

# This is used to authenticate and see if the credentials of user/password-hashed_password exists in the database
# If credentials exist we return the user object which has all the data about the user else return False.
def authenticate_user(username: str, password: str, db: db_dependency):
    logger.info("Authenticating user")
    user = db.query(Users).filter(Users.username == username).first()
    if not user: # If user is None, i.e. there is no user in the database
        logger.warning("User doesn't exist in the database")
        return False
    if not bcrypt_context.verify(password, user.hashed_password): # Checks if the password from the token matches user password from the database 
        logger.warning("Wrong password")
        return False
    return user

# Creates the access json web token for a standardized way to securely send data between two parties
def create_access_token(username: str, user_id: int, country: str, age: int, expires_delta: timedelta):
    logger.info(f"Creating a jwt token for user id: {user_id}")
    encode = {'sub': username, 'id': user_id, 'country': country, 'age': age} # This is the payload information
    expires = datetime.utcnow() + expires_delta # Expiry time of the json token
    encode.update({'exp': expires})
    logger.info(f"Created a jwt token for user: {user_id}")
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM) # We specify the algorithm to encode the json token and the encrypt the json token using secret key, and then pass the payload for the json token

# This function is used to decode jwt and verify if user retreived from the jwt, exists in the database or not.
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub') # Username specified in 'encode' of create_access_token
        user_id: int = payload.get('id') # User_id specified in 'encode' of create_access_token
        country: str = payload.get('country')
        age: str = payload.get('age')
        logger.info(f"Got the jwt payload for user id: {user_id}")
        if username is None or user_id is None:
            logger.info(f"Could validate credentials of user id: {user_id}, from the database")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate credentials of user')
        
        logger.info(f"Validated the user: {user_id} successfully")
        return {'username' : username, 'id': user_id, 'country': country, 'age': age}
    except JWTError:
        logger.error("JWT error occured")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

# Creates a user with it's important credentials
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    # create_user_model = Users(**create_user_request.model_dump()) # Isn't used as we specified in our validation class as 'password' here as 'hashed_password'
    logger.info("Adding a user to the database")
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        age=create_user_request.age,
        hashed_password=bcrypt_context.hash(create_user_request.password), # Here the password is encoded
        country=create_user_request.country
    )
    logger.info(f"Successfully created a user: {create_user_model.id}and added to the database")
    db.add(create_user_model)
    db.commit()

# Verfication of token is done. If the verification is successful then return the token code which is used to transmit the data.
# form_data -> Is the json web token format which has the 
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        logger.warning("User validation unsuccessful")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(user.username, user.id, user.country, user.age, timedelta(hours=24))
    logger.info(f"Login is successful for user: {user.id}")
    return {'access_token' : token, 'token_type' : 'bearer'}
