from pydantic import BaseModel

class PaginationMeta(BaseModel):
    page: int
    limit: int
    total_items: int
    total_pages: int