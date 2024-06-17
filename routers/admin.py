import os
from sqlalchemy import cast, String, Integer
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from schema.models import Shows, ShowsVerify, rating_to_age
from schema.database import SessionLocal
from auth.owner import get_super_user
from passlib.context import CryptContext
import dotenv
from logs.app_logger import get_logger
logger = get_logger(__name__)

router = APIRouter(
    prefix='/netflix',
    tags=['netflix']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
admin_dependency = Annotated[dict, Depends(get_super_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class AdminVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=4)

# Getting the env variable
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(admin: admin_dependency, db: db_dependency):
    logger.info("Accessing the whole catalog of shows in database")
    if admin is None:
        logger.warning("Not logged in as admin")
        raise HTTPException(status_code=401, details='Authentication Failed')
    return db.query(Shows).filter(cast(Shows.show_id, Integer) <= 100).all()

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_show(admin: admin_dependency, db: db_dependency,
                      show_request: ShowsVerify):
    logger.info("Adding a show to the database")
    if admin is None:
        logger.warning("Not logged in as admin")
        raise HTTPException(status_code=401, details='Authentication Failed')

    try:
        logger.info("Adding a show to the catalog")
        show_model = Shows(**show_request.model_dump(), age_rating=rating_to_age[show_request.model_dump()['rating']])
    except KeyError:
        logger.error("Wrong age rating specified")
        return f"Wrong Age rating entered.\nAvailable age ratings are: {rating_to_age.keys()}"
    
    db.add(show_model)
    db.commit()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(admin: admin_dependency, db: db_dependency,
                          admin_verification: AdminVerification):
    logger.info(f"Changing the password for admin")
    if admin is None:
        logger.warning("Not logged in as admin")
        raise HTTPException(status_code=401, detail='Authentication Failed')

    hashed_password = bcrypt_context.hash(os.environ["ADMIN_PASSWORD"])
    if not bcrypt_context.verify(admin_verification.password, hashed_password):
        logger.warning("Authentication failed, failed to change the password for admin")
        raise HTTPException(status_code=401, detail='Error on the password change')
    
    logger.info(f"Successfully changed the password for admin")
    os.environ["ADMIN_PASSWORD"] = admin_verification.new_password
    dotenv.set_key(dotenv_file, "ADMIN_PASSWORD", os.environ["ADMIN_PASSWORD"])



@router.put("/update/{show_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_show(admin: admin_dependency, db: db_dependency,
                      show_request: ShowsVerify,
                      show_id: int = Path(gt=0)):
    logger.info(f"Updating a show with show_id: {show_id} in database")
    if admin is None:
        logger.warning("Not logged in as admin")
        raise HTTPException(status_code=401, details='Authentication Failed')
    
    show_model = db.query(Shows).filter(Shows.show_id == show_id).first()
    if show_model is None:
        logger.info(f"The show isn't available in the database. Hence can't update")
        raise HTTPException(status_code=404, detail='show isnt available in your country or its inappropriate for your age')
    
    show_model.type=show_request.type
    show_model.title=show_request.title
    show_model.director=show_request.director
    show_model.cast=show_request.cast
    show_model.country=show_request.country
    show_model.date_added=show_request.date_added
    show_model.release_year=show_request.release_year
    show_model.rating=show_request.rating
    show_model.duration=show_request.duration
    show_model.listed_in=show_request.listed_in
    show_model.description=show_request.description
    try:
     show_model.age_rating=rating_to_age[show_request.model_dump()['rating']]
    except KeyError:
        logger.error("Wrong age rating specified")
        return f"Wrong Age rating entered.\nAvailable age ratings are: {rating_to_age.keys()}"

    logger.info("Successfully updated the show in the database")
    db.add(show_model)
    db.commit()


@router.delete("/show/{show_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_show(admin: admin_dependency, db: db_dependency, show_id: int = Path(gt=0)):
    logger.info(f"Deleting show with show id: {show_id} from the database")
    if admin is None:
        logger.warning("Not logged in as admin")
        raise HTTPException(status_code=401, details='Authentication Failed')
    
    show_model = db.query(Shows).first()
    if show_model is None:
        logger.info(f"The show isn't available in the database. Hence can't delete")
        raise HTTPException(status_code=404, detail='show isnt available in your country or its inappropriate for your age')
    
    logger.info("Successfully deleted the show")
    db.query(Shows).filter(Shows.show_id == show_id).delete()
    db.commit()