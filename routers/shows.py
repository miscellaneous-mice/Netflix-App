from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import cast, String, Integer
from starlette import status
from schema.models import Shows
from schema.database import SessionLocal
from auth.auth import get_current_user
# from mongo_database import add_history, find_history
from datetime import date, datetime
from logs.app_logger import get_logger
logger = get_logger(__name__)

router = APIRouter(
    prefix='/shows',
    tags=['Shows']
)


def get_db():
    db = SessionLocal()
    logger.info("Starting a local database session")
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        logger.error("Authentication failed")
        raise HTTPException(status_code=401, details='Authentication Failed')
    
    logger.info("Browsing all available shows")
    return db.query(Shows).filter(cast(Shows.show_id, Integer) <= 100)\
    .filter(cast(Shows.country, String) == cast(user.get('country'), String)).filter(cast(Shows.age_rating, Integer) < cast(user.get('age'), Integer)).all()


@router.get("/search/{show_id}", status_code=status.HTTP_200_OK)
async def read_show(user: user_dependency, db: db_dependency, show_id: int = Path(gt=0)):
    if user is None:
        logger.error("Authentication failed")
        raise HTTPException(status_code=401, details='Authentication Failed')
    
    logger.info(f"Watching show with show id: {show_id}")
    show_model = db.query(Shows).filter(cast(Shows.show_id, Integer) == cast(show_id, Integer))\
        .filter(cast(Shows.country, String) == cast(user.get('country'), String)).filter(cast(Shows.age_rating, Integer) < cast(user.get('age'), Integer)).first()
    
    if show_model is not None:
        today = date.today()
        # add_history(user_id=user.get('id'), show_id=show_model.show_id, watch_date=today.strftime("%d-%m-%Y"))
        logger.info(f"Watched show with show id: {show_id}")
        return show_model
    
    logger.info(f"Show isn't available for the person due to age restriction or availability in his/her country")
    raise HTTPException(status_code=404, detail='show isnt available in your country or its inappropriate for your age')


# @router.get("/history", status_code=status.HTTP_200_OK)
# async def get_user_history(user: user_dependency):
#     if user is None:
#         logger.error("Authentication failed")
#         raise HTTPException(status_code=401, details='Authentication Failed')
    
#     # logger.info(f"Got the watch history for user: {user.get('id')}")
#     # return user.get('id')
#     history = find_history(int(user.get('id')))
#     logger.info(f"Got the watch history for user: {user.get('id')}")
#     return history.get('watch_history')

def valid_date_format(str_date):
    try:
        fmt_date = datetime.strptime(str_date.strip(), '%Y-%m-%d')
        return fmt_date
    except Exception as e:
        return False

@router.get("/date_added", status_code=status.HTTP_200_OK)
async def filter_show_by_date_added(user: user_dependency, db: db_dependency, 
                                    start_date: str, end_date: str):
    if user is None:
        raise HTTPException(status_code=401, details='Authentication Failed')
    
    start_date = valid_date_format(start_date)
    end_date = valid_date_format(end_date)

    if not start_date and not end_date:
        show_model = []
    elif not start_date and end_date:
        show_model = db.query(Shows).filter(Shows.date_added <= end_date)\
        .filter(Shows.country == user.get('country')).filter(Shows.age_rating < user.get('age')).first()
    elif start_date and not end_date:
        show_model = db.query(Shows).filter(Shows.date_added >= start_date)\
        .filter(Shows.country == user.get('country')).filter(Shows.age_rating < user.get('age')).first()
    else:
        show_model = db.query(Shows).filter(Shows.date_added >= start_date).filter(Shows.date_added <= end_date)\
        .filter(Shows.country == user.get('country')).filter(Shows.age_rating < user.get('age')).first()

    if show_model is not None:
        return show_model
    raise HTTPException(status_code=404, detail='show isnt available in date range specified in your country for your age')


# @router.get("/show/recommendations", status_code=status.HTTP_200_OK)
# async def filter_show_by_release_year(user: user_dependency, db: db_dependency, 
#                                       genre: str, duration: str, content_type: str):
#     if user is None:
#         raise HTTPException(status_code=401, details='Authentication Failed')
#     birth_year = date.today().year - user.get('age')

#     show_model = db.query(Shows).filter(Shows.release_year >= birth_year)\
#     .filter(Shows.country == user.get('country')).filter(Shows.age_rating < user.get('age')).first()

#     if show_model is not None:
#         return show_model
#     raise HTTPException(status_code=404, detail='show isnt available in release year specified in\
#                          your country for your age')
