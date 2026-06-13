from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


class AuthService:

    @staticmethod
    def register_user(
        db: Session,
        full_name: str,
        email: str,
        password: str
    ):

        existing_user = UserRepository.get_by_email(
            db,
            email
        )

        if existing_user:
            raise ValueError(
                "Email already exists"
            )

        password_hash = hash_password(
            password
        )

        user = UserRepository.create_user(
            db,
            full_name,
            email,
            password_hash
        )

        return user

    @staticmethod
    def login_user(
        db: Session,
        email: str,
        password: str
    ):

        user = UserRepository.get_by_email(
            db,
            email
        )

        if not user:
            raise ValueError(
                "Invalid email or password"
            )

        is_valid = verify_password(
            password,
            user.PasswordHash
        )

        if not is_valid:
            raise ValueError(
                "Invalid email or password"
            )

        token = create_access_token(
            {
                "sub": user.Email,
                "user_id": user.UserId
            }
        )

        return token