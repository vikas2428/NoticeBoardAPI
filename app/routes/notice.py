from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import FileResponse

from app.services.notice_service import notice_service
from app.schemas.notice_schema import NoticeCreate, NoticeUpdate

from app.utils.notice_iterator import (
    NoticeIterator,
    notice_generator
)

from app.utils.file_handler import file_handler
from app.services.analytics_service import analytics_service
from app.services.async_service import process_notices_async
from app.dependencies import get_notice_service
from app.utils.decorators import log_execution_time

from fastapi import Depends


router = APIRouter()


# ============================================================
# CREATE NOTICE
# ============================================================

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


# ============================================================
# GET ALL NOTICES
# ============================================================

@router.get("/notices")
async def get_notices():
    """
    Get all non-deleted notices.
    """

    return notice_service.get_all_notices()
# ============================================================
# GET ARCHIVED NOTICES
# ============================================================
@router.get("/notices/archived")
async def get_archived_notices():
    return notice_service.get_archived_notices()

# ============================================================
# GET RECENTLY DELETED NOTICES
# ============================================================

@router.get("/notices/deleted")
async def get_deleted_notices():
    return notice_service.get_deleted_notices()

# ============================================================
# SEARCH NOTICES
# ============================================================

@router.get("/notices/search")
async def search_notices(
    keyword: str | None = Query(
        None,
        min_length=1,
        max_length=100,
        description="Search in title, description, or category"
    ),
    category: str | None = Query(
        None,
        min_length=1,
        max_length=50,
        description="Filter by category"
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


# ============================================================
# UPDATE NOTICE
# ============================================================

@router.put("/notices/{notice_id}")
async def update_notice(
    notice_id: int,
    notice: NoticeUpdate
):
    """
    Update an existing notice.
    """

    existing_notice = notice_service.get_notice_by_id(
        notice_id
    )

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


# ============================================================
# ARCHIVE NOTICE
# ============================================================

@router.patch("/notices/{notice_id}/archive")
async def archive_notice(notice_id: int):
    """
    Archive a notice.
    """

    notice = notice_service.get_notice_by_id(
        notice_id
    )

    if notice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found"
        )

    if notice["deleted_at"] is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot archive a deleted notice"
        )

    archived_notice = notice_service.archive_notice(
        notice_id
    )

    return {
        "message": "Notice archived successfully",
        "notice": archived_notice
    }
# ============================================================
# UNARCHIVE NOTICE
# ============================================================

@router.patch("/notices/{notice_id}/unarchive")
async def unarchive_notice(notice_id: int):

    notice = notice_service.get_notice_by_id(notice_id)

    if notice is None:
        raise HTTPException(
            status_code=404,
            detail="Notice not found"
        )

    if notice["deleted_at"] is not None:
        raise HTTPException(
            status_code=400,
            detail="Notice is in Recently Deleted"
        )

    if notice["status"] != "Archived":
        raise HTTPException(
            status_code=400,
            detail="Notice is not archived"
        )

    restored_notice = notice_service.unarchive_notice(
        notice_id
    )

    return {
        "message": "Notice unarchived successfully",
        "notice": restored_notice
    }


# ============================================================
# MOVE NOTICE TO RECENTLY DELETED
# ============================================================

@router.delete("/notices/{notice_id}")
async def delete_notice(notice_id: int):
    """
    Move a notice to Recently Deleted.

    This is a soft delete.
    The notice remains in the database.
    """

    notice = notice_service.get_notice_by_id(
        notice_id
    )

    if notice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found"
        )

    if notice["deleted_at"] is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Notice is already in Recently Deleted"
        )

    deleted_notice = notice_service.delete_notice(
        notice_id
    )

    return {
        "message": "Notice moved to Recently Deleted",
        "notice": deleted_notice
    }
# ============================================================
# RESTORE NOTICE FROM RECENTLY DELETED
# ============================================================

# ============================================================
# RESTORE NOTICE FROM RECENTLY DELETED
# ============================================================

@router.patch("/notices/{notice_id}/restore")
async def restore_notice(notice_id: int):
    """
    Restore a notice from Recently Deleted.
    The notice is moved back to Active status.
    """

    notice = notice_service.get_notice_by_id(notice_id)

    if notice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found"
        )

    if notice["deleted_at"] is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Notice is not in Recently Deleted"
        )

    restored_notice = notice_service.restore_notice(
        notice_id
    )

    return {
        "message": "Notice restored successfully",
        "notice": restored_notice
    }

# ============================================================
# PERMANENTLY DELETE NOTICE
# ============================================================

@router.delete("/notices/{notice_id}/permanent")
async def permanently_delete_notice(notice_id: int):
    """
    Permanently delete a notice from the database.
    """

    notice = notice_service.get_notice_by_id(
        notice_id
    )

    if notice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found"
        )

    notice_service.permanently_delete_notice(
        notice_id
    )

    return {
        "message": "Notice permanently deleted"
    }


# ============================================================
# EXPORT JSON
# ============================================================

@router.get("/notices/export/json")
async def export_notices_json():
    """
    Export all non-deleted notices as JSON.
    """

    notices = notice_service.get_all_notices()

    file_path = file_handler.export_json(
        notices
    )

    return FileResponse(
        path=file_path,
        media_type="application/json",
        filename="notices.json"
    )


# ============================================================
# EXPORT CSV
# ============================================================

@router.get("/notices/export/csv")
async def export_notices_csv():
    """
    Export all non-deleted notices as CSV.
    """

    notices = notice_service.get_all_notices()

    file_path = file_handler.export_csv(
        notices
    )

    return FileResponse(
        path=file_path,
        media_type="text/csv",
        filename="notices.csv"
    )


# ============================================================
# EXPORT TXT
# ============================================================

@router.get("/notices/export/txt")
async def export_notices_txt():
    """
    Export all non-deleted notices as TXT.
    """

    notices = notice_service.get_all_notices()

    file_path = file_handler.export_txt(
        notices
    )

    return FileResponse(
        path=file_path,
        media_type="text/plain",
        filename="notices.txt"
    )


# ============================================================
# ANALYTICS
# ============================================================

@router.get("/notices/analytics")
@log_execution_time
async def get_notice_analytics(
    service=Depends(get_notice_service)
):
    """
    Get notice statistics and analytics.
    """

    notices = service.get_all_notices()

    return analytics_service.get_statistics(
        notices
    )


# ============================================================
# ITERATOR & GENERATOR PROCESSING
# ============================================================

@router.get("/notices/processing")
async def process_notices():
    """
    Demonstrate iterator and generator processing.
    """

    notices = notice_service.get_all_notices()

    # Custom iterator
    iterator = NoticeIterator(notices)

    iterator_titles = []

    for notice in iterator:
        iterator_titles.append(
            notice["title"]
        )

    # Generator
    generator_titles = []

    for notice in notice_generator(notices):
        generator_titles.append(
            notice["title"]
        )

    return {
        "iterator_result": iterator_titles,
        "generator_result": generator_titles,
        "total_processed": len(notices)
    }


# ============================================================
# ASYNC PROCESSING
# ============================================================

@router.get("/notices/async-processing")
async def async_process_notices():
    """
    Process notices concurrently using asyncio.
    """

    notices = notice_service.get_all_notices()

    processed_notices = await process_notices_async(
        notices
    )

    return {
        "method": "asyncio.gather",
        "total_processed": len(processed_notices),
        "results": processed_notices
    }
# ============================================================
# GET SINGLE NOTICE
# ============================================================

@router.get("/notices/{notice_id}")
async def get_notice(notice_id: int):
    """
    Get a single notice by ID.
    """

    notice = notice_service.get_notice_by_id(notice_id)

    if notice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found"
        )

    return notice

