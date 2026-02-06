from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class SourceBase(BaseModel):
    url: str
    domain: str
    title: Optional[str] = None
    snippet: Optional[str] = None
    source_type: Optional[str] = "web"
    domain_age_days: Optional[int] = None
    wauback_url: Optional[str] = None

    class Config:
        from_attributes = True

class ClaimInput(BaseModel):
    text: str

class ClaimResponse(BaseModel):
    id: int
    text: str
    status: str
    created_at: datetime
    credibility_score: Optional[float] = None
    credibility_label: Optional[str] = None
    explanation: Optional[str] = None
    summary: Optional[str] = None
    entities: Optional[List[Any]] = None
    sources: List[SourceBase] = []

    class Config:
        from_attributes = True
