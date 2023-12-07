from typing import Optional

from pydantic import BaseModel


class Example(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
