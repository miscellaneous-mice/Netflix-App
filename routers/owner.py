import os
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from pydantic import BaseModel
from passlib.context import CryptContext
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime
import dotenv
from logs.app_logger import get_logger
logger = get_logger(__name__)
# All the requests will be prependded with /auth/
router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

# Getting the env variable
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

# Secret key and algorithm used in JWT tokens
SECRET_KEY = 'n2PgwN86khjrEfuPmPow9leIUMsl7iV6'
ALGORITHM = 'HS256'

# Configuration used for hashing passwords
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Used to authenticate every request used to access todo database for their respective databases
oauth2_bearer_admin = OAuth2PasswordBearer(tokenUrl='admin/token',
                                           scheme_name="admin_oauth2_schema")

# Used for Data validation of our token as to which format our json format of token should be like
class Token(BaseModel):
    access_token: str
    token_type: str

def authenticate_admin(username: str, password: str):
    logger.info("Autheticating admin access")
    user = {'username': username, 'password': password}
    hashed_password = bcrypt_context.hash(os.environ["ADMIN_PASSWORD"])

    if (user.get('username') != 'Netflix') or\
          not(bcrypt_context.verify(user.get('password'), hashed_password)): 
        logger.warning("Admin access failed")
        return False
    
    logger.info("Admin access successful")
    return user


def create_access_token(expires_delta: timedelta):
    logger.info("Creating jwt token for admin access")
    encode = {'info': 'You have complete access to catalog of shows'} # This is the payload information
    expires = datetime.utcnow() + expires_delta # Expiry time of the json token
    encode.update({'exp': expires})
    logger.info("Successfully created jwt token for admin access")
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM) # We specify the algorithm to encode the json token and the encrypt the json token using secret key, and then pass the payload for the json token


async def get_super_user(token: Annotated[str, Depends(oauth2_bearer_admin)]):
    try:
        logger.info("Successfully received the jwt token for the admin access")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        info: str = payload.get('info') # Username specified in 'encode' of create_access_token
        return {'message' : info}
    except JWTError:
        logger.error("JWT token error during admin access")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate admin')


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    logger.info("Logging in for admin access")
    user = authenticate_admin(form_data.username, form_data.password)
    if not user:
        logger.warning("Couldn't authenticate the admin")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Youre not the Admin')
    token = create_access_token(timedelta(hours=24))
    logger.info("Successfully created logged in for admin access.")
    return {'access_token' : token, 'token_type' : 'bearer'}