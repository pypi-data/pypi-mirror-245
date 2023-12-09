from dataclasses import dataclass

from .enums import AnimationFormat, Element, IconFormat


@dataclass
class LichWeapon:
    """Represents a lich weapon."""

    id: str
    """The ID of the weapon."""
    url_name: str
    """The URL name of the weapon."""
    icon: str
    """The icon URL of the weapon."""
    icon_format: IconFormat
    """The format of the weapon's icon."""
    thumb: str
    """The thumbnail URL of the weapon."""
    item_name: str
    """The name of the weapon."""


@dataclass
class LichEphemera:
    """Represents a lich ephemera."""

    id: str
    """The ID of the ephemera."""
    url_name: str
    """The URL name of the ephemera."""
    icon: str
    """The icon URL of the ephemera."""
    icon_format: IconFormat
    """The format of the ephemera's icon."""
    thumb: str
    """The thumbnail URL of the ephemera."""
    animation: str
    """The animation URL of the ephemera."""
    animation_format: AnimationFormat
    """The format of the ephemera's animation."""
    element: Element
    """The element of the ephemera."""
    item_name: str
    """The name of the ephemera."""


@dataclass
class LichQuirk:
    """Represents a lich quirk."""

    id: str
    """The ID of the quirk."""
    url_name: str
    """The URL name of the quirk."""
    item_name: str
    """The name of the quirk."""
    description: str
    """The description of the quirk."""
    group: str
    """The group of the quirk. Does not belong to any specific enum"""
