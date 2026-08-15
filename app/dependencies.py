from app.services.notice_service import notice_service


def get_notice_service():
    """
    FastAPI dependency that provides the NoticeService.
    """

    return notice_service