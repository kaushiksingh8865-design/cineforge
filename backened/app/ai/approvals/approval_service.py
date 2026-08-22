from backened.app.ai.proposal.proposal import Proposal
from cineforge.backened.app.ai.schemas.approval import ApprovalDecision



def approve_proposal(
    proposal: Proposal,
    reviewer: str,
    comment: str = "",
) -> ApprovalDecision:
    return ApprovalDecision(
        proposal_id=proposal.proposal_id,
        approved=True,
        reviewer=reviewer,
        comment=comment,
    )



def reject_proposal(
    proposal: Proposal,
    reviewer: str,
    comment: str = "",
) -> ApprovalDecision:
    return ApprovalDecision(
        proposal_id=proposal.proposal_id,
        approved=False,
        reviewer=reviewer,
        comment=comment,
    )