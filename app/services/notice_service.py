from datetime import datetime

from app.database.database import database


class NoticeService:
    """
    Business logic for Notice Board API.
    """

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

    def get_all_notices(self):
        """
        Return only active notices ordered by newest first.
        """

        query = """
        SELECT
            id,
            title,
            description,
            category,
            created_at,
            expiry_date,
            status
        FROM notices
        WHERE status = 'Active'
        ORDER BY id DESC
        """

        notices = database.fetch_all(query)

        return [dict(notice) for notice in notices]

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
            status
        FROM notices
        WHERE id = ?
        """

        notice = database.fetch_one(query, (notice_id,))

        if notice is None:
            return None

        return dict(notice)

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
                str(notice.expiry_date) if notice.expiry_date else None,
                notice_id
            )
        )

        return self.get_notice_by_id(notice_id)
    def delete_notice(self, notice_id: int):
        """
        Delete a notice by ID.
        """

        # Check whether notice exists
        notice = self.get_notice_by_id(notice_id)

        if notice is None:
            return False

        query = """
        DELETE FROM notices
        WHERE id = ?
        """

        database.execute(query, (notice_id,))

        return True
    
        def archive_notice(self, notice_id: int):
            """
            Archive a notice without permanently deleting it.
            """

            query = """
            UPDATE notices
            SET status = ?
            WHERE id = ?
            """

            database.execute(
                query,
                (
                    "Archived",
                    notice_id
                )
            )

        return self.get_notice_by_id(notice_id)

    def search_notices(self, keyword: str = None, category: str = None):
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
            status
        FROM notices
        WHERE status = 'Active'
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


# Singleton instance
notice_service = NoticeService()