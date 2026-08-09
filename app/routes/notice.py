from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import FileResponse

from app.schemas.notice_schema import NoticeCreate, NoticeUpdate
from app.services.notice_service import notice_service
from app.utils.file_handler import file_handler

router = APIRouter()


@router.post(
    "/notices",
    status_code=status.HTTP_201_CREATED
)
async def create_notice(notice: NoticeCreate):
    """
    Create a new notice.
    """

    notice_id = notice_service.create_notice(notice)

    return {
        "message": "Notice created successfully",
        "notice_id": notice_id
    }


@router.get("/notices")
async def get_all_notices():
    """
    Get all active notices.
    """

    return notice_service.get_all_notices()


@router.get("/notices/search")
async def search_notices(
    keyword: str = Query(
        ...,
        min_length=1,
        max_length=100,
        description="Keyword to search in title, description, or category"
    )
):
    """
    Search active notices by keyword.
    """

    notices = notice_service.search_notices(keyword)

    return {
        "keyword": keyword,
        "count": len(notices),
        "results": notices
    }


@router.get("/notices/search")
async def search_notices(
    keyword: str | None = Query(
        None,
        min_length=1,
        max_length=100,
        description="Keyword to search in title, description, or category"
    ),
    category: str | None = Query(
        None,
        min_length=1,
        max_length=50,
        description="Filter notices by category"
    )
):
    """
    Search active notices by keyword and/or category.
    """

    if keyword is None and category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a keyword or category"
        )

    notices = notice_service.search_notices(
        keyword=keyword,
        category=category
    )

    return {
        "keyword": keyword,
        "category": category,
        "count": len(notices),
        "results": notices
    }

@router.get("/notices/export/json")
async def export_notices_json():
    """
    Export all active notices as a JSON file.
    """

    notices = notice_service.get_all_notices()

    file_path = file_handler.export_json(notices)

    return FileResponse(
        path=file_path,
        media_type="application/json",
        filename="notices.json"
    )
@router.get("/notices/export/csv")
async def export_notices_csv():
    """
    Export all active notices as a CSV file.
    """

    notices = notice_service.get_all_notices()

    file_path = file_handler.export_csv(notices)

    return FileResponse(
        path=file_path,
        media_type="text/csv",
        filename="notices.csv"
    )

@router.get("/notices/export/txt")
async def export_notices_txt():
    """
    Export all active notices as a text file.
    """

    notices = notice_service.get_all_notices()

    file_path = file_handler.export_txt(notices)

    return FileResponse(
        path=file_path,
        media_type="text/plain",
        filename="notices.txt"
    )

@router.put("/notices/{notice_id}")
async def update_notice(
    notice_id: int,
    notice: NoticeUpdate
):
    """
    Update an existing notice.
    """

    existing_notice = notice_service.get_notice_by_id(notice_id)

    if existing_notice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found"
        )

    updated_notice = notice_service.update_notice(
        notice_id,
        notice
    )

    return {
        "message": "Notice updated successfully",
        "notice": updated_notice
    }


@router.patch("/notices/{notice_id}/archive")
async def archive_notice(notice_id: int):
    """
    Archive a notice without deleting it.
    """

    notice = notice_service.get_notice_by_id(notice_id)

    if notice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found"
        )

    archived_notice = notice_service.archive_notice(notice_id)

    return {
        "message": "Notice archived successfully",
        "notice": archived_notice
    }