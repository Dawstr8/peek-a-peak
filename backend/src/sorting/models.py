from typing import Optional

from pydantic import BaseModel


class SortParams(BaseModel):
    sort_by: Optional[str] = None
    order: Optional[str] = None
