from dataclasses import dataclass


@dataclass
class Notice:
    id: int
    title: str
    description: str
    category: str
    created_at: str
    expiry_date: str | None
    status: str