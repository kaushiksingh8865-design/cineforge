from typing import Literal

from pydantic import BaseModel, Field


class ContinuityFinding(BaseModel):
    category: str = Field(
        description="The type of continuity issue, such as character, prop, scene, or other."
    )
    severity: Literal["low", "medium", "high"] = Field(
        description="How serious the potential continuity issue is."
    )
    message: str = Field(
        description="A concise explanation of the potential continuity issue."
    )
    evidence: list[str] = Field(
        default_factory=list,
        description="Facts from the supplied continuity context supporting the finding."
    )
    recommendation: str | None = Field(
        default=None,
        description="A possible recommendation for the filmmaker, if appropriate."
    )


class ContinuityAnalysis(BaseModel):
    summary: str = Field(
        description="A concise summary of the continuity analysis."
    )
    findings: list[ContinuityFinding] = Field(
        default_factory=list,
        description="Potential continuity issues found in the supplied context."
    )