from dataclasses import dataclass

from pytenno.models.enums import ItemRarity, DropSourceType

from .missions import DroptableMission, DroptableNPC, DroptableRelic


@dataclass
class DropTable:
    """Represents an item's drop table."""

    missions: list[DroptableMission]
    """The missions where the item can be found."""
    relics: list[DroptableRelic]
    """The relic in which parts for the item can be found."""
    npc: list[DroptableNPC]
    """The NPCs where the item can be found."""

    def _from_data(node: dict):
        return DropTable(
            [DroptableMission._from_data(mission) for mission in node["missions"]],
            [DroptableRelic._from_data(relic) for relic in node["relics"]],
            [DroptableNPC._from_data(npc) for npc in node["npc"]],
        )


@dataclass
class Drop:
    """Represents an item's drop."""

    name: str
    """The translated name of the location / item."""
    link: str
    """Link to the internal or extarnal source with information about that location."""


@dataclass
class RelicRates:
    """Reprents a relic's chance for an item at varius rarities"""

    intact: float
    exceptional: float
    flawless: float
    radiant: float


@dataclass
class DropSource:
    """Represents a drop source for an item"""

    type: DropSourceType
    """The type of the drop source"""
    item: str
    """The ID of the item dropped"""
    relic: str
    """The ID of the relic where  parts for the item can be found."""
    rates: RelicRates
    """Chance(s) that the item can be found under the conditions of a relic."""
    rarity: ItemRarity
    """The rariry of the item."""
    id: str
    """The ID of the drop source"""

    def _from_data(data: dict):
        return DropSource(
            type=data.pop("type"),
            item=data.pop("item"),
            relic=data.pop("relic"),
            rates=RelicRates(**data.pop("rates")),
            rarity=ItemRarity[data.pop("rarity")],
            id=data.pop("id"),
        )
