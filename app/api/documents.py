from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.document_schema import (
    DocumentCreateRequest,
    DocumentUpdateRequest
)
from app.services.document_service import DocumentService
from app.dependencies.auth_dependency import get_current_user

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


# CREATE
@router.post("")
def create_document(
    data: DocumentCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    try:

        document = DocumentService.create_document(
            db,
            current_user["user_id"],
            data.document_name,
            data.expiry_date,
            data.reminder_days
        )

        return {
            "message": "Document created successfully",
            "tracker_id": document.TrackerId
        }

    except ValueError as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )


# GET ALL
@router.get("")
def get_documents(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return DocumentService.get_documents(
        db,
        current_user["user_id"]
    )


# DASHBOARD
@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return DocumentService.get_dashboard_stats(
        db,
        current_user["user_id"]
    )


# ✅ EXPIRY ALERTS
@router.get("/alerts")
def get_expiry_alerts(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return DocumentService.get_expiry_alerts(
        db,
        current_user["user_id"]
    )


# FILE VIEW
@router.get("/{tracker_id}/file")
def get_document_file(
    tracker_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    try:

        return DocumentService.get_document_file(
            db,
            tracker_id,
            current_user["user_id"]
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )


# GET SINGLE
@router.get("/{tracker_id}")
def get_document(
    tracker_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    try:

        return DocumentService.get_document(
            db,
            tracker_id,
            current_user["user_id"]
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )


# UPDATE
@router.put("/{tracker_id}")
def update_document(
    tracker_id: int,
    data: DocumentUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    try:

        return DocumentService.update_document(
            db,
            tracker_id,
            current_user["user_id"],
            data.document_name,
            data.expiry_date,
            data.reminder_days
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )


# DELETE
@router.delete("/{tracker_id}")
def delete_document(
    tracker_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    try:

        DocumentService.delete_document(
            db,
            tracker_id,
            current_user["user_id"]
        )

        return {
            "message": "Document deleted successfully"
        }

    except ValueError as ex:

        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )