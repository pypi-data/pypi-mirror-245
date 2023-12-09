"""Module for utility functions used elsewhere in the pytenno package.

    Some of these functions are used to convert data types to and from
    their respective JSON representations.

    There are also a handful of user-friendly functions for common
    tasks, such as converting a string to a valid url-safe string.
"""


import datetime
from enum import Enum
from typing import Any, Callable, Mapping, Type, TypeVar
from urllib.parse import quote

import aiohttp

from .constants import ASSET_ROOT, VALID_TRANSLATIONS_RAW
from .errors import BaseError
from .models.droptable import Drop, RelicRates
from .models.enums import (AnimationFormat, AuctionMarking, AuctionType,
                           Element, Faction, IconFormat, ItemRarity,
                           MeasurementUnit, OrderType, PatreonBadge, Platform,
                           Polarity, RivenAttributeGroup, RivenWeaponGroup,
                           RivenWeaponType, Rotation, Stage, Subtype, UserRole,
                           UserStatus)


def format_name(name: str):
    """Converts a string to a valid url-safe string."""
    return quote(name.lower().replace(" ", "_"))


def is_formatted_name(name: str):
    """Checks if a string is a valid formatted name."""
    return quote(name.replace("_", " ").lower()) == name


def _raise_error_code(response: aiohttp.ClientResponse, silenced: list[Exception]):
    """Raises an error based on the response's status code."""
    code = response.status

    for error in BaseError.__subclasses__():
        if error.code == code:
            if error not in silenced:
                raise error
            return None

    error = BaseError
    error.code = code
    error.msg = "Unknown error occurred"

    raise error


DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S.%f%z"


# Enums that take in a value and return an enum value
_ENUM_MAPPING: Mapping[str, Type[Enum]] = {
    "rarity": ItemRarity,
    "order_type": OrderType,
    "element": Element,
    "patreon_badge": PatreonBadge,
    "platform": Platform,
    "role": UserRole,
    "status": UserStatus,
    "polarity": Polarity,
    "riven_type": RivenWeaponType,
    "icon_format": IconFormat,
    "animation_format": AnimationFormat,
    "rotation": Rotation,
    "type": AuctionType,
    "is_marked_for": AuctionMarking,
    "faction": Faction,
}

# Enums that require special attention
_SPECIAL_ENUM_MAPPING: Mapping[str, Callable[[str], Type[Enum]]] = {
    "subtypes": lambda names: [Subtype[name] for name in names],
    "exclusive_to": lambda excls: [RivenWeaponGroup[exc] for exc in excls],
    "units": lambda unit: MeasurementUnit[unit],
    "group": lambda grp: RivenAttributeGroup[
        grp
    ]  # The API is ambigous on this attribute; three different items have the name but can have different values
    if hasattr(RivenAttributeGroup, grp)
    else RivenWeaponGroup[grp]
    if hasattr(RivenWeaponGroup, grp)
    else grp,
    "stage": lambda stage: Stage[f"_{stage}" if stage.isdigit() else stage],
    "is_marked_for": lambda mark: AuctionMarking[mark] if mark is not None else None,
    "rates": lambda rates: RelicRates(**rates),
}

T = TypeVar("T", bound=type)


def _from_data(
    cls_: Type[T], data: dict[str, Any] | list[dict[str, Any]] | None, use_data_method: bool = True
) -> T:
    """Partially converts common data types into their object equivalent, then creates an instance of ``cls_``."""
    if data is None:
        return None
    
    if isinstance(data, list):
        for d in data:
            d = _format_names(d)
    else:
        data = _format_names(data)

    if hasattr(cls_, "_from_data") and use_data_method:
        return cls_._from_data(data)
    return cls_(**data)


def _format_names(d: dict):
    nd = {}  # Create new dict to avoid RuntimeErrors
    for key, value in d.items():
        if value is None:
            continue
        if key in ("icon", "sub_icon", "thumb", "avatar", "animation", "background"):
            nd[key] = f"{ASSET_ROOT}/{value}"
        elif key in (
            "creation_date",
            "created",
            "last_updated",
            "last_update",
            "updated",
            "last_seen",
            "marked_operation_at",
        ):
            nd[key] = datetime.datetime.strptime(value, DATETIME_FORMAT)
        elif key == "drop":
            nd[key] = [Drop(**val) for val in value]
        elif key in {"zh-hans", "zh-hant"}:
            nd[{"zh-hans": "zh_hans", "zh-hant": "zh_hant"}[key]] = value
        else:
            try:
                nd[key] = _ENUM_MAPPING[key][value]
            except KeyError:
                try:
                    nd[key] = _SPECIAL_ENUM_MAPPING[key](value)
                except KeyError:
                    nd[key] = value
    return nd

