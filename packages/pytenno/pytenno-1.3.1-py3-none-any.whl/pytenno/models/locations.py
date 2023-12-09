from dataclasses import dataclass

from .enums import Faction


@dataclass
class Location:
    """Represents a location."""

    id: str
    """The ID of the location."""
    icon: str
    """The icon URL of the location."""
    thumb: str
    """The thumbnail URL of the location."""
    faction: Faction
    """The faction of the location."""
    name: str
    """The name of the location."""
    node_name: str
    """The name of the node the location is on."""
