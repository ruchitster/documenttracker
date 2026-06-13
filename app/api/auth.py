from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.schemas.auth_schema import (
    RegisterRequest,
    LoginRequest
)

from app.services.auth_service import AuthService

from app.core.database import get_db

from app.dependencies.auth_dependency import (
    get_current_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    try:

        user = AuthService.register_user(
            db,
            data.full_name,
            data.email,
            data.password
        )

        return {
            "message": "User registered successfully",
            "user_id": user.UserId
        }

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    try:

        token = AuthService.login_user(
            db,
            data.email,
            data.password
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except ValueError as ex:

        raise HTTPException(
            status_code=401,
            detail=str(ex)
        )


@router.get("/me")
def me(
    current_user=Depends(
        get_current_user
    )
):

    return {
        "user": current_user
    }