from typing import Literal

from pydantic import BaseModel, Field


class ResearchFinding(BaseModel):
    claim: str = Field(
        description="A factual claim relevant to the research question."
    )

    evidence: str = Field(
        description="Evidence supporting the claim."
    )

    source: str = Field(
        description="The source or reference supporting the evidence."
    )

    confidence: Literal["low", "medium", "high"] = Field(
        description="Confidence that the finding is accurate and well-supported."
    )


class ResearchResult(BaseModel):
    summary: str = Field(
        description="A concise summary of the research findings."
    )

    findings: list[ResearchFinding] = Field(
        default_factory=list,
        description="Evidence-based findings relevant to the research question."
    )