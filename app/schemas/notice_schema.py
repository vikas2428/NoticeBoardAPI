from datetime import date
from pydantic import BaseModel, Field


class NoticeCreate(BaseModel):
    """
    Schema used when creating a new notice.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=200
    )

    description: str = Field(
        ...,
        min_length=1
    )

    category: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    expiry_date: date | None = None


class NoticeUpdate(BaseModel):
    """
    Schema used when updating an existing notice.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=200
    )

    description: str = Field(
        ...,
        min_length=1
    )

    category: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    expiry_date: date | None = None