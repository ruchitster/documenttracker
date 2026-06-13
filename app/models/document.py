from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Boolean,
    ForeignKey
)

from sqlalchemy.sql import func

from app.core.database import Base


class DocumentTracker(Base):
    __tablename__ = "DocumentTracker"

    TrackerId = Column(
        Integer,
        primary_key=True,
        index=True
    )

    UserId = Column(
        Integer,
        ForeignKey("Users.UserId"),
        nullable=False
    )

    DocumentName = Column(
        String(200),
        nullable=False
    )

    ExpiryDate = Column(
        Date,
        nullable=False
    )

    ReminderDays = Column(
        Integer,
        nullable=False
    )

    FilePath = Column(
        String(500),
        nullable=True
    )

    FileType = Column(
        String(50),
        nullable=True
    )

    IsActive = Column(
        Boolean,
        default=True
    )

    CreatedDate = Column(
        DateTime,
        server_default=func.getdate()
    )

    UpdatedDate = Column(
        DateTime,
        nullable=True
    )