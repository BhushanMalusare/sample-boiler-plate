from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import JWT_KEY
from logger import setup_logging
from models import UserCredentialsDatabaseModel
from routers.v1 import schemas

logger = setup_logging()

# Initialize the CryptContext
pwd_context = CryptContext(
    schemes=["bcrypt_sha256"],
    deprecated="auto",
)


# User Credential Verification
def validate_user_credentials(user_credentials: schemas.Login, db: Session):
    # Query the user_credentials table for the provided email
    user = (
        db.query(UserCredentialsDatabaseModel)
        .filter(UserCredentialsDatabaseModel.email == user_credentials.email)
        .first()
    )
    if user and pwd_context.verify(user_credentials.password, user.password):
        return True
    else:
        return False


def user_authentication(user_credentials, db: Session):  # schemas.Login
    # Password hashing context
    if validate_user_credentials(user_credentials, db):
        # Generate a JWT token for the authenticated user
        token = jwt.encode(
            {"email": user_credentials.email}, JWT_KEY, algorithm="HS256"
        )
        logger.info(f"Token generated for user {user_credentials.email}")
        return {"token": token}
    else:
        logger.error(f"Invalid credentials for user:- {user_credentials.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
