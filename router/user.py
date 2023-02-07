from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_database_session
from schemas.user import User as UserSchema, ShowUser as ShowUserSchema
from models.user import User as UserModel
from hashing import encrypt
from utils import validate_email

router = APIRouter(tags=["User"], prefix="/user")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(request: UserSchema, db: Session = Depends(get_database_session)):
    try:
        if not validate_email(request.email):
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is not valid"
            )
        hashed_password = encrypt(request.password)
        new_user = UserModel(
            name=request.name, email=request.email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "name": request.name,
            "email": request.email
        }
    except Exception as e:
        print("EXCEPTION: ", e)
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occured or user already exists",
        )
