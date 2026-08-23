from datetime import datetime

from app.database.database import database


class NoticeService:
    """
    Business logic for Notice Board API.
    """

    # --------------------------------------------------
    # CREATE NOTICE
    # --------------------------------------------------

    def create_notice(self, notice):
        """
        Create a new notice.
        """

        query = """
        INSERT INTO notices
        (
            title,
            description,
            category,
            created_at,
            expiry_date,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """

        notice_id = database.execute(
            query,
            (
                notice.title,
                notice.description,
                notice.category,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                str(notice.expiry_date) if notice.expiry_date else None,
                "Active"
            )
        )

        return notice_id

    # --------------------------------------------------
    # GET SINGLE NOTICE
    # --------------------------------------------------

    def get_notice_by_id(self, notice_id: int):
        """
        Return a single notice by ID.
        """

        query = """
        SELECT
            id,
            title,
            description,
            category,
            created_at,
            expiry_date,
            status,
            deleted_at
        FROM notices
        WHERE id = ?
        """

        notice = database.fetch_one(
            query,
            (notice_id,)
        )

        if notice is None:
            return None

        return dict(notice)

    # --------------------------------------------------
    # GET ALL ACTIVE / NON-DELETED NOTICES
    # --------------------------------------------------

    def get_all_notices(self):
        """
        Return all notices that are not permanently deleted.
        """

        query = """
        SELECT
            id,
            title,
            description,
            category,
            created_at,
            expiry_date,
            status,
            deleted_at
        FROM notices
        WHERE deleted_at IS NULL
        ORDER BY id DESC
        """

        notices = database.fetch_all(query)

        return [dict(notice) for notice in notices]

    # --------------------------------------------------
    # GET ARCHIVED NOTICES
    # --------------------------------------------------

    def get_archived_notices(self):
        """
        Return all archived notices.
        """

        query = """
        SELECT
            id,
            title,
            description,
            category,
            created_at,
            expiry_date,
            status,
            deleted_at
        FROM notices
        WHERE status = 'Archived'
        AND deleted_at IS NULL
        ORDER BY id DESC
        """

        notices = database.fetch_all(query)

        return [dict(notice) for notice in notices]

    def unarchive_notice(self, notice_id: int):
        """
        Move an archived notice back to Active.
        This does NOT delete the notice.
        """

        query = """
        UPDATE notices
        SET status = 'Active'
        WHERE id = ?
        AND status = 'Archived'
        AND deleted_at IS NULL
        """

        database.execute(query, (notice_id,))

        return self.get_notice_by_id(notice_id)
    # --------------------------------------------------
    # ARCHIVE NOTICE
    # --------------------------------------------------

    def archive_notice(self, notice_id: int):
        """
        Archive a notice.
        """

        query = """
        UPDATE notices
        SET status = 'Archived'
        WHERE id = ?
        AND deleted_at IS NULL
        """

        database.execute(
            query,
            (notice_id,)
        )

        return self.get_notice_by_id(notice_id)

    # --------------------------------------------------
    # MOVE TO RECENTLY DELETED
    # --------------------------------------------------

    def delete_notice(self, notice_id: int):
        """
        Move a notice to Recently Deleted.
        This is a soft delete.
        """

        query = """
        UPDATE notices
        SET deleted_at = CURRENT_TIMESTAMP
        WHERE id = ?
        AND deleted_at IS NULL
        """

        database.execute(
            query,
            (notice_id,)
        )

        return self.get_notice_by_id(notice_id)

    # --------------------------------------------------
    # GET RECENTLY DELETED NOTICES
    # --------------------------------------------------

    def get_deleted_notices(self):
        """
        Return all notices in Recently Deleted.
        """

        query = """
        SELECT
            id,
            title,
            description,
            category,
            created_at,
            expiry_date,
            status,
            deleted_at
        FROM notices
        WHERE deleted_at IS NOT NULL
        ORDER BY deleted_at DESC
        """

        notices = database.fetch_all(query)

        return [dict(notice) for notice in notices]

    # --------------------------------------------------
    # RESTORE DELETED NOTICE
    # --------------------------------------------------

    def restore_notice(self, notice_id: int):
        """
        Restore a notice from Recently Deleted.
        """

        query = """
        UPDATE notices
        SET
            deleted_at = NULL,
            status = 'Active'
        WHERE id = ?
        AND deleted_at IS NOT NULL
        """

        database.execute(
            query,
            (notice_id,)
        )

        return self.get_notice_by_id(notice_id)

    # --------------------------------------------------
    # PERMANENT DELETE
    # --------------------------------------------------

    def permanently_delete_notice(self, notice_id: int):
        """
        Permanently delete a notice from the database.
        """

        query = """
        DELETE FROM notices
        WHERE id = ?
        """

        database.execute(
            query,
            (notice_id,)
        )

        return True

    # --------------------------------------------------
    # UPDATE NOTICE
    # --------------------------------------------------

    def update_notice(self, notice_id: int, notice):
        """
        Update an existing notice.
        """

        query = """
        UPDATE notices
        SET
            title = ?,
            description = ?,
            category = ?,
            expiry_date = ?
        WHERE id = ?
        """

        database.execute(
            query,
            (
                notice.title,
                notice.description,
                notice.category,
                str(notice.expiry_date)
                if notice.expiry_date
                else None,
                notice_id
            )
        )

        return self.get_notice_by_id(notice_id)

    # --------------------------------------------------
    # SEARCH NOTICES
    # --------------------------------------------------

    def search_notices(
        self,
        keyword: str = None,
        category: str = None
    ):
        """
        Search active notices by keyword and/or category.
        """

        query = """
        SELECT
            id,
            title,
            description,
            category,
            created_at,
            expiry_date,
            status,
            deleted_at
        FROM notices
        WHERE status = 'Active'
        AND deleted_at IS NULL
        """

        parameters = []

        if keyword:
            query += """
            AND (
                title LIKE ?
                OR description LIKE ?
                OR category LIKE ?
            )
            """

            search_pattern = f"%{keyword.strip()}%"

            parameters.extend([
                search_pattern,
                search_pattern,
                search_pattern
            ])

        if category:
            query += """
            AND category LIKE ?
            """

            parameters.append(
                f"%{category.strip()}%"
            )

        query += """
        ORDER BY id DESC
        """

        notices = database.fetch_all(
            query,
            tuple(parameters)
        )

        return [dict(notice) for notice in notices]


# --------------------------------------------------
# SINGLETON INSTANCE
# --------------------------------------------------

notice_service = NoticeService()