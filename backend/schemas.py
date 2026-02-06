from typing import List, Optional, Any
from pydantic import BaseModel
from datetime import datetime

# Input
class ClaimInput(BaseModel):
    text: str

# Output
class SourceBase(BaseModel):
    url: str
    domain: str
    title: Optional[str] = None
    snippet: Optional[str] = None
    published_at: Optional[datetime] = None
    source_type: Optional[str] = "unknown"

class ClaimResponse(BaseModel):
    id: int
    text: str
    status: str
    created_at: datetime
    entities: Optional[List[Any]] = None
    summary: Optional[str] = None
    credibility_score: Optional[int] = None
    credibility_label: Optional[str] = None
    explanation: Optional[str] = None
    sources: List[SourceBase] = []

    class Config:
        from_attributes = True
