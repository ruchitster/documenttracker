from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
import os

from app.core.database import get_db
from app.dependencies.auth_dependency import get_current_user
from app.repositories.document_repository import DocumentRepository

router = APIRouter(
    prefix="/documents",
    tags=["Documents Upload"]
)

UPLOAD_FOLDER = "uploads/documents"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/{tracker_id}/upload")
async def upload_document(
    tracker_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    document = DocumentRepository.get_document_by_id(db, tracker_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document.UserId != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    # =========================
    # FIX 1: safe filename
    # =========================
    extension = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid4()}{extension}"

    # =========================
    # FIX 2: FORCE FORWARD SLASH PATH
    # =========================
    relative_path = f"uploads/documents/{unique_name}"
    full_path = os.path.join(UPLOAD_FOLDER, unique_name)

    # save file
    with open(full_path, "wb") as buffer:
        buffer.write(await file.read())

    # store in DB (IMPORTANT FIX)
    document.FilePath = relative_path
    document.FileType = file.content_type

    db.commit()

    return {
        "message": "File uploaded successfully",
        "file_path": relative_path,
        "file_type": file.content_type
    }