from dataclasses import dataclass
from datetime import datetime

from ..utils import _from_data
from .enums import PatreonBadge, Platform, UserRole, UserStatus


@dataclass
class PatreonProfile:
    """Represents a Patreon profile."""

    patreon_founder: bool
    """Whether the user is a Patreon founder."""
    subscription: bool
    """Whether the user is a Patreon subscriber."""
    patreon_badge: PatreonBadge | None = None
    """The Patreon badge of the user, if any."""


@dataclass
class BaseUser:
    """Base class that other user classes inherit from."""

    id: str
    """The ID of the user."""
    ingame_name: str
    """The ingame name of the user."""
    region: str
    """The region the user is on."""
    avatar: str | None = None
    """The URL of the user's avatar, if any."""

    def __repr__(self):
        return f"<User id={self.id} ingame_name={self.ingame_name}>"


@dataclass
class LinkedProfiles:
    """Represents a user's linked profiles."""

    discord_profile: bool
    """Whether the user has a Discord profile linked to their warframe.market profile."""
    patreon_profile: bool
    """Whether the user has a Patreon profile linked to their warframe.market profile."""
    xbox_profile: bool
    """Whether the user has a Xbox profile linked to their warframe.market profile."""
    steam_profile: bool
    """Whether the user has a Steam profile linked to their warframe.market profile."""
    github_profile: bool
    """Whether the user has a GitHub profile linked to their warframe.market profile."""

@dataclass(kw_only=True)
class CurrentUser(BaseUser):
    """Represents the current user. This is the user that is logged in."""

    anonymous: bool
    """Whether the user is anonymous."""
    verification: bool
    """Whether the user is verified."""
    check_code: str
    """The check / verification code of the user."""
    role: UserRole
    """The role of the user."""
    platform: Platform
    """The platform of the user."""
    banned: bool
    """Whether the user is banned."""
    ban_reason: str | None = None
    """The reason the user is banned. If None, the user is not banned."""
    background: str | None = None
    """The URL of the user's background. If None, the user has no background."""
    has_mail: bool
    """Whether the user has unread mail."""
    reputation: int
    """The reputation of the user."""
    linked_accounts: LinkedProfiles
    """The linked accounts of the user."""
    patreon_profile: PatreonProfile
    """The Patreon profile of the user."""
    written_reviews: int
    """The number of reviews the user has written today."""
    unread_messages: int
    """The number of unread messages the user has."""

    def _from_data(node: dict):
        return CurrentUser(
            # file deepcode ignore WrongNumberOfArguments
            patreon_profile=_from_data(PatreonProfile, node.pop("patreon_profile")),
            linked_accounts=LinkedProfiles(**node.pop("linked_accounts")),
            **node,
        )


@dataclass(kw_only=True)
class UserShort(BaseUser):
    """Represents a user."""

    status: UserStatus
    """The status of the user."""
    reputation: int
    """The reputation of the user."""
    last_seen: datetime | None
    """The last time the user was seen. If None, the user has not been seen."""
