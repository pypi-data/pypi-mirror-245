from dataclasses import dataclass, field

from .enums import (IconFormat, MeasurementUnit, RivenAttributeGroup,
                    RivenWeaponGroup, RivenWeaponType)


@dataclass
class RivenItem:
    """Represents a riven item."""

    id: str
    """The ID of the riven item."""
    item_name: str
    """The name of the riven item."""
    url_name: str
    """The URL name of the riven item."""
    group: RivenWeaponGroup
    """The group of the riven item."""
    riven_type: RivenWeaponType
    """The type of the riven item."""
    icon: str
    """The icon URL of the riven item."""
    icon_format: IconFormat
    """The format of the icon URL of the riven item."""
    thumb: str
    """The thumbnail URL of the riven item."""


@dataclass(kw_only=True)
class RivenAttribute:
    """Represents a riven attribute. Most rivens have multiple attributes."""

    id: str
    """The ID of the riven attribute."""
    url_name: str
    """The URL name of the riven attribute."""
    group: RivenAttributeGroup
    """The group of the riven attribute."""
    prefix: str = field(default="")
    """The prefix of the riven attribute. Default is empty string."""
    suffix: str = field(default="")
    """The suffix of the riven attribute. Default is empty string."""
    positive_is_negative: bool
    """Whether the positive attribute is actually negative."""
    exclusive_to: list[RivenWeaponType] | None = None
    """The types of weapons that the attribute is exclusive to. Default is None, meaning it is not exclusive to any weapon."""
    effect: str
    """The name of the effect of the riven attribute. Depends on the requested language."""
    units: MeasurementUnit | None = None
    """The units of the riven attribute. Default is None, meaning it is not measured in any units."""
    negative_only: bool
    """Whether the attribute only appears as a negative."""
    search_only: bool
    """Whether the attribute only appears in search results."""


@dataclass
class PartialRivenAttribute:
    """Represents a partial riven attribute."""

    positive: bool
    """Whether the attribute is positive."""
    value: int
    """The value of the attribute."""
    url_name: str
    """The URL name of the attribute."""
