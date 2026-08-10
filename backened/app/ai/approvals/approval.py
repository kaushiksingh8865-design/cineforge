from pydantic import BaseModel
class ApprovalDecision(BaseModel):
    proposal_id:str
    approved:bool
    reviewer:str
    comment:str =""


