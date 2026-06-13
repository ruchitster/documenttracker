from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ):
        return (
            db.query(User)
            .filter(User.Email == email)
            .first()
        )

    @staticmethod
    def create_user(
        db: Session,
        full_name: str,
        email: str,
        password_hash: str
    ):

        user = User(
            FullName=full_name,
            Email=email,
            PasswordHash=password_hash
        )

        db.add(user)

        db.commit()

        db.refresh(user)

        return user