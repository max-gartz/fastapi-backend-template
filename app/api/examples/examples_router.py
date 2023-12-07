from typing import List

from fastapi import APIRouter

from app.core.examples.examples_schema import Example

router = APIRouter(prefix="/examples", tags=["examples"])


@router.get("", response_model=List[Example])
def get_examples() -> List[Example]:
    """Get examples."""
    return [
        Example(id=1, name="example1"),
        Example(id=2, name="example2", description="example2 description")
    ]
