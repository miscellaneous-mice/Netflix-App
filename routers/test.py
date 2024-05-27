# from models import Shows
import time
from shows import user_dependency
from starlette import status
from fastapi import HTTPException, APIRouter, Path
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
# from routers.caching import exportable_cache
from functools import cache

router = APIRouter(
    prefix='/test',
    tags=['Test Queries']
)

class JSON(BaseModel):
    data: str

class Fact(BaseModel):
    low: int = Field(ge=1)
    high: int = Field(lt=100000)

    class Config:
        json_schema_extra = {
                'example' : {
                    'low' : 20000,
                    'high' : 20100
                }
        }

# @exportable_cache
@cache
def factorial(n):
    result = 1
    for i in range(1, n+1):
        result *= i
    return result

@router.get("/", status_code=status.HTTP_200_OK)
async def sample_get():
    return "Just testing some code"

@router.post("/performance", status_code=status.HTTP_200_OK)
async def sample_factorial(inputs: Fact):
    input_range = inputs.model_dump()
    start = time.time()
    print("Computing.....")
    for x in range(input_range['low'], input_range['high']):
        factorial(x)
    end = time.time()
    return f"Execution time: {end - start}"


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def sample_post(json: JSON)-> JSONResponse: 
    data_model = json.model_dump()
    return JSONResponse( 
         status_code=status.HTTP_200_OK, 
         content={"detail": str(data_model)}, 
     )

@router.get("/about", status_code=status.HTTP_200_OK)
async def get_owner_id(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, details='Authentication Failed')
    return user