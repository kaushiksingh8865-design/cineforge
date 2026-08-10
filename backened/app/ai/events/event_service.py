from datetime import datetime
from uuid import uuid4

from .event import Event


def create_event(
    event_type: str,
    description: str,
    proposal_id: str,
) -> Event:
    return Event(
        event_id=str(uuid4()),
        event_type=event_type,
        description=description,
        timestamp=datetime.now(),
        proposal_id=proposal_id,
    )
if __name__ == "__main__":
    event = create_event(
        event_type="PROPOSAL_APPROVED",
        description="Scene 12 location change was approved.",
        proposal_id="p-001",
    )

    print(event)