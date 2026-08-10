from backened.app.ai.proposal.proposal import Proposal
from backened.app.ai.approvals.approval_service import approve_proposal, reject_proposal

proposal = Proposal(
    proposal_id="p-001",
    description="Change Scene 12 location.",
    reason="Better visual continuity.",
    status="pending",
)

approved = approve_proposal(
    proposal,
    reviewer="director",
    comment="Looks good.",
)

rejected = reject_proposal(
    proposal,
    reviewer="director",
    comment="Keep the original location.",
)

print("Approved:", approved)
print("Rejected:", rejected)
