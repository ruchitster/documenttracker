from app.repositories.document_repository import DocumentRepository


class DocumentService:

    @staticmethod
    def create_document(
        db,
        user_id,
        document_name,
        expiry_date,
        reminder_days
    ):

        if reminder_days < 0:
            raise ValueError(
                "Reminder days cannot be negative"
            )

        return DocumentRepository.create_document(
            db,
            user_id,
            document_name,
            expiry_date,
            reminder_days
        )

    @staticmethod
    def get_documents(
        db,
        user_id
    ):

        return DocumentRepository.get_documents_by_user(
            db,
            user_id
        )

    @staticmethod
    def get_document(
        db,
        tracker_id,
        user_id
    ):

        document = (
            DocumentRepository.get_document_by_id(
                db,
                tracker_id
            )
        )

        if not document:
            raise ValueError(
                "Document not found"
            )

        if document.UserId != user_id:
            raise ValueError(
                "Access denied"
            )

        return document

    @staticmethod
    def update_document(
        db,
        tracker_id,
        user_id,
        document_name,
        expiry_date,
        reminder_days
    ):

        document = (
            DocumentRepository.get_document_by_id(
                db,
                tracker_id
            )
        )

        if not document:
            raise ValueError(
                "Document not found"
            )

        if document.UserId != user_id:
            raise ValueError(
                "Access denied"
            )

        return (
            DocumentRepository.update_document(
                db,
                document,
                document_name,
                expiry_date,
                reminder_days
            )
        )

    @staticmethod
    def delete_document(
        db,
        tracker_id,
        user_id
    ):

        document = (
            DocumentRepository.get_document_by_id(
                db,
                tracker_id
            )
        )

        if not document:
            raise ValueError(
                "Document not found"
            )

        if document.UserId != user_id:
            raise ValueError(
                "Access denied"
            )

        return (
            DocumentRepository.delete_document(
                db,
                document
            )
        )

    # ==========================
    # DASHBOARD STATS
    # ==========================
    @staticmethod
    def get_dashboard_stats(
        db,
        user_id
    ):

        return (
            DocumentRepository.get_dashboard_stats(
                db,
                user_id
            )
        )

    # ==========================
    # EXPIRY ALERTS
    # ==========================
    @staticmethod
    def get_expiry_alerts(
        db,
        user_id
    ):

        return (
            DocumentRepository.get_expiry_alerts(
                db,
                user_id
            )
        )

    # ==========================
    # FILE VIEW
    # ==========================
    @staticmethod
    def get_document_file(
        db,
        tracker_id,
        user_id
    ):

        document = (
            DocumentRepository.get_document_file(
                db,
                tracker_id
            )
        )

        if not document:
            raise ValueError(
                "Document not found"
            )

        if document.UserId != user_id:
            raise ValueError(
                "Access denied"
            )

        return {
            "file_path": document.FilePath,
            "file_type": document.FileType
        }