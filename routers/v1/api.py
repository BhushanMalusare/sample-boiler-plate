from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.orm import Session

from dependencies import get_db
from logger import setup_logging
from routers.v1 import schemas
from routers.v1.crud import authentication, recommender

logger = setup_logging()  # Getting a logger instance with the current module's name

# initializing fast api app
router = APIRouter(prefix="/v1")


# endpoint to authenticate user
@router.post("/auth", response_model=schemas.LoginResponse)
def authenticate_user(user_credentials: schemas.Login, db=Depends(get_db)):
    data = authentication.user_authentication(user_credentials, db)
    return data


# endpoint to get recommend temps based on city and state
@router.get("/recommend-temp", response_model=schemas.TempRecommendations)
def temp_recommender(
    authorization: str = Header(...),
    city: str = Query(..., min_length=36, max_length=36),
    state: str = Query(..., min_length=36, max_length=36),
    speciality: str = Query(..., min_length=36, max_length=36),
    certificate: str = Query(..., min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    data = recommender.temp_recommender(
        authorization=authorization,
        city=city,
        state=state,
        speciality=speciality,
        certificate=certificate,
        db=db,
    )
    return data


# endpoint to recommend shifts to temps based on city, state, speciality and certificate
@router.get("/recommend-shifts", response_model=schemas.ShiftDataRecommendations)
def shift_recommender(
    # request: Request,
    authorization: str = Header(...),
    city: str = Query(..., min_length=36, max_length=36),
    state: str = Query(..., min_length=36, max_length=36),
    speciality: str = Query(..., min_length=36, max_length=36),
    certificate: str = Query(..., min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    data = recommender.shift_recommender(
        authorization=authorization,
        city=city,
        state=state,
        speciality=speciality,
        certificate=certificate,
        db=db,
    )
    return data
