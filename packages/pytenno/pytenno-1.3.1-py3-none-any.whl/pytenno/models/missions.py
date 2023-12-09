from dataclasses import dataclass

from .enums import ItemRarity, RelicQuality, Rotation, Stage, Subtype


@dataclass
class DroptableRelic:
    """Represents a relic drop in a mission"""

    id: str
    """The ID of the relic."""
    rarity: ItemRarity
    """The rarity of the item found in the relic."""
    rate: dict[RelicQuality, int | float]
    """A mapping of relic quality to the rate of the relic dropping."""


@dataclass
class DroptableNPC:
    """Represents a NPC in a mission"""

    id: str
    """The ID of the NPC."""
    icon: str
    """The icon URL of the NPC."""
    thumb: str
    """The thumbnail URL of the NPC."""
    name: str
    """The name of the NPC."""


@dataclass
class DroptableMission:
    """Represents a mission."""

    mission_id: str
    """The ID of the mission."""
    node_id: str
    """The ID of the node the mission is on."""
    rarity: ItemRarity
    """The rarity of the item found in the mission."""
    rate: int | float
    """The rate of the item found in the mission."""
    item_subtype: Subtype
    """The subtype of the item found in the mission."""
    rotation: Rotation
    """The rotation where the item can be found."""
    stage: Stage
    """The stage of the item found in the mission."""
    relics: list[DroptableRelic]
    """Relics that can be found in the mission."""
    npc: list[DroptableNPC]
    """The NPCs where the item can be found."""


@dataclass
class PartialMission:
    """Represents a partial mission."""

    id: str
    """The ID of the mission."""
    icon: str
    """The icon URL of the mission."""
    thumb: str
    """The thumbnail URL of the mission."""
    name: str
    """The name of the mission."""
