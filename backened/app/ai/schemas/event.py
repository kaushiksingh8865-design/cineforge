from datetime import datetime
from pydantic import BaseModel


class Event(BaseModel):
    event_id: str
    event_type: str
    description: str
    timestamp: datetime
    proposal_id: str