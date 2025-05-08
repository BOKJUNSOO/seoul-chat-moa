from pydantic import Field , BaseModel
from datetime import date, datetime
from typing import List, Optional


# response field
class Location(BaseModel):
    name: str
    gu: str = Field(...,alias="gu")
    station: str = Field(...,alias="station")


class Event(BaseModel):
    eventId: str = Field(..., alias="event_id")
    title: str
    category: str
    location: Location
    startDate: date = Field(..., alias="start_date")
    endDate: date = Field(..., alias="end_date")

class Meta(BaseModel):
    queryDate: date
    limit: int
    returned: int
    timestamp: datetime

class APIResponse(BaseModel):
    success: bool
    meta: Meta
    data: List[Event]
    result: Optional[str] = None

# request field
class ChatRequest(BaseModel):
    prompt: str = Field(..., description="사용자 입력 프롬프트")
    limit: int = Field(2, ge=1, le=10, description="가져올 행사 개수")