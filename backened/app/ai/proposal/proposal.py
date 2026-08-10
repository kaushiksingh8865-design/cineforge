from pydantic import BaseModel

class Proposal(BaseModel):  
    proposal_id: str
    description: str
    reason: str
    status: str

