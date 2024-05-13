from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator


# Pydantic model for user credentials
class Login(BaseModel):
    email: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=50)

    @field_validator("email")
    @classmethod
    def valid_email(cls, email):
        try:
            valid = validate_email(email)
            return valid.email
        except EmailNotValidError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
            )


# login response model
class LoginResponse(BaseModel):
    token: str


# temps recommendations response model
class TempRecommendationsSchema(BaseModel):
    health_care_supporter: list = Field(alias="Health Care supporter")
    care_specialist: list = Field(alias="Care Specialist")
    patient_advocate: list = Field(alias="Patient Advocate")
    clinical_excellence: list = Field(alias="Clinical Excellence")
    elite_care_partner: list = Field(alias="Elite Care Partner")

    class Config:
        allow_population_by_field_name = True


class TempsDataRecommendation(BaseModel):
    temps: TempRecommendationsSchema


class TempRecommendations(BaseModel):
    data: TempsDataRecommendation


# shift recommendation response model
class ShiftRecommendationSchema(BaseModel):
    shift: list = Field(alias="shift")

    class Config:
        allow_population_by_field_name = True


class ShiftDataRecommendations(BaseModel):
    data: ShiftRecommendationSchema
