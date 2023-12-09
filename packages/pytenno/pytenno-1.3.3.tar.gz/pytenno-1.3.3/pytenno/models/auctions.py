from dataclasses import dataclass
from datetime import datetime
from typing import Union

from ..utils import _from_data
from .enums import AuctionMarking, AuctionType, Element, Platform, Polarity
from .rivens import PartialRivenAttribute
from .users import UserShort


@dataclass(kw_only=True)
class AuctionEntry:
    """Represents an auction entry."""

    id: str
    """The ID of the auction entry."""
    minimal_reputation: int
    """The minimal reputation required to bid on the auction."""
    winner: str | None = None
    """The ID of the winner of the auction, if any."""
    private: bool
    """Whether the auction is private or not."""
    visible: bool
    """Whether the auction is visible or not."""
    note_raw: str
    """The raw note of the auction."""
    note: str
    """The note of the auction entry."""
    owner: str
    """The ID of the owner of the auction."""
    starting_price: int
    """The starting price of the auction."""
    buyout_price: int | None = None
    """The buyout price of the auction, if any."""
    minimal_increment: int | None = None
    """The minimal increment for bids, if any."""
    is_direct_sell: bool
    """Whether the auction is a direct sell or not."""
    top_bid: int | None = None
    """The highest bid on the auction, if any."""
    created: datetime
    """The date and time the auction was created."""
    updated: datetime
    """The date and time the auction entry was created."""
    platform: Platform
    """The platform the auction is on."""
    closed: bool
    """Whether the auction is closed or not."""
    is_marked_for: AuctionMarking | None = None
    """Whether the auction is marked for a specific action."""
    marked_operation_for: datetime | None = None
    """The time when the auction was marked for a specific operation."""
    item: Union["RivenAuction", "LichAuction", "KubrowAuction"]
    """The item of the auction."""


@dataclass
class AuctionEntryExpanded(AuctionEntry):
    """Same as `AuctionEntry`, but with a full user model for ``.owner``"""

    owner: UserShort
    """The owner of the auction."""

    def _from_data(node: dict):
        # deepcode ignore
        return AuctionEntryExpanded(
            # file deepcode ignore WrongNumberOfArguments
            owner=_from_data(UserShort, node.pop("owner")),
            item=_from_data(RivenAuction, item)
            if (t := (item := node.pop("item"))["type"]) == "riven"
            else _from_data(LichAuction, item)
            if t == "lich"
            else _from_data(KubrowAuction, item),
            **node,
        )


@dataclass(kw_only=True)
class LichAuction:
    """Represents a lich auction."""

    type: AuctionType  # lich
    """The type of the auction. In this case, ``lich``."""
    weapon_url_name: str
    """The URL name of the weapon."""
    element: Element
    """The element of the weapon."""
    damage: int
    """The damage of the weapon."""
    having_ephemera: bool
    """Whether the weapon has an ephemera."""
    quirk: str | None = None
    """The quirk of the lich, if any."""
    name: str | None = None
    """The name of the lich. Unused by the API."""


@dataclass
class KubrowAuction:
    """Represents a kubrow auction."""

    type: AuctionType
    """The type of the auction. In this case, ``kubrow``."""
    name: str
    """The name of the kubrow."""


@dataclass
class RivenAuction:
    """Represents a riven auction."""

    type: AuctionType
    """The type of the auction. In this case, ``riven``."""
    attributes: list[PartialRivenAttribute]
    """The attributes of the riven."""
    name: str
    """The name of the riven."""
    mastery_level: int
    """The mastery level of the riven."""
    re_rolls: int
    """The number of times the riven has been rerolled."""
    weapon_url_name: str
    """The URL of the weapon the riven is for."""
    polarity: Polarity
    """The polarity of the riven."""
    mod_rank: int
    """The rank of the riven."""

    def _from_data(node: dict):
        return RivenAuction(
            attributes=[
                _from_data(PartialRivenAttribute, x) for x in node.pop("attributes")
            ],
            **node,
        )
