from pydantic import BaseModel
from app.ai.schemas.statechange import StateChange

class Proposal(BaseModel):  
    proposal_id: str
    description: str
    reason: str
    status: str
    change : StateChange

