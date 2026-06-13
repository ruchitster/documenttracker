from datetime import date, timedelta

from app.models.document import DocumentTracker


class DocumentRepository:

    @staticmethod
    def create_document(
        db,
        user_id,
        document_name,
        expiry_date,
        reminder_days
    ):

        document = DocumentTracker(
            UserId=user_id,
            DocumentName=document_name,
            ExpiryDate=expiry_date,
            ReminderDays=reminder_days
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    @staticmethod
    def get_documents_by_user(
        db,
        user_id
    ):

        return (
            db.query(DocumentTracker)
            .filter(
                DocumentTracker.UserId == user_id,
                DocumentTracker.IsActive == True
            )
            .all()
        )

    @staticmethod
    def get_document_by_id(
        db,
        tracker_id
    ):

        return (
            db.query(DocumentTracker)
            .filter(
                DocumentTracker.TrackerId == tracker_id
            )
            .first()
        )

    @staticmethod
    def update_document(
        db,
        document,
        document_name,
        expiry_date,
        reminder_days
    ):

        document.DocumentName = document_name
        document.ExpiryDate = expiry_date
        document.ReminderDays = reminder_days

        db.commit()
        db.refresh(document)

        return document

    @staticmethod
    def delete_document(
        db,
        document
    ):

        document.IsActive = False

        db.commit()

        return True

    # ==========================
    # DASHBOARD
    # ==========================
    @staticmethod
    def get_dashboard_stats(
        db,
        user_id
    ):

        today = date.today()
        seven_days = today + timedelta(days=7)
        thirty_days = today + timedelta(days=30)

        documents = (
            db.query(DocumentTracker)
            .filter(
                DocumentTracker.UserId == user_id,
                DocumentTracker.IsActive == True
            )
            .all()
        )

        return {
            "total_documents": len(documents),

            "expired_documents": len([
                d for d in documents
                if d.ExpiryDate < today
            ]),

            "expiring_in_7_days": len([
                d for d in documents
                if today <= d.ExpiryDate <= seven_days
            ]),

            "expiring_in_30_days": len([
                d for d in documents
                if today <= d.ExpiryDate <= thirty_days
            ])
        }

    # ==========================
    # FILE VIEW
    # ==========================
    @staticmethod
    def get_document_file(
        db,
        tracker_id
    ):

        return (
            db.query(DocumentTracker)
            .filter(
                DocumentTracker.TrackerId == tracker_id,
                DocumentTracker.IsActive == True
            )
            .first()
        )

    # ==========================
    # EXPIRY ALERTS
    # ==========================
    @staticmethod
    def get_expiry_alerts(
        db,
        user_id
    ):

        documents = (
            db.query(DocumentTracker)
            .filter(
                DocumentTracker.UserId == user_id,
                DocumentTracker.IsActive == True
            )
            .all()
        )

        today = date.today()

        alerts = []

        for document in documents:

            if not document.ExpiryDate:
                continue

            days_left = (
                document.ExpiryDate - today
            ).days

            # Expired
            if days_left < 0:

                alerts.append({
                    "tracker_id": document.TrackerId,
                    "document_name": document.DocumentName,
                    "days_left": days_left,
                    "status": "expired"
                })

            # Reminder period reached
            elif days_left <= document.ReminderDays:

                alerts.append({
                    "tracker_id": document.TrackerId,
                    "document_name": document.DocumentName,
                    "days_left": days_left,
                    "status": "expiring"
                })

        alerts.sort(
            key=lambda x: x["days_left"]
        )

        return alerts