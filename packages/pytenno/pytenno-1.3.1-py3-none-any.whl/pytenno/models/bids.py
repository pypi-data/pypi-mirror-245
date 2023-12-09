from dataclasses import dataclass
from datetime import datetime


@dataclass
class Bid:
    """Represents a bid on an auction."""

    id: str
    """The ID of the bid."""
    auction: str
    """The ID of the auction the bid is on."""
    user: str
    """The ID of the user who made the bid."""
    value: int
    """The value (platinum) of the bid."""
    created: datetime
    """The date and time the bid was created."""
    updated: datetime
    """The date and time the bid was updated."""
