from pydantic import BaseModel
from datetime import date


class DocumentCreateRequest(BaseModel):
    document_name: str
    expiry_date: date
    reminder_days: int


class DocumentUpdateRequest(BaseModel):
    document_name: str
    expiry_date: date
    reminder_days: int


class DocumentResponse(BaseModel):
    TrackerId: int
    DocumentName: str
    ExpiryDate: date
    ReminderDays: int

    class Config:
        from_attributes = True