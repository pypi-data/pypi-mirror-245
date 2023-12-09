"""Small module for constants used throughout the PyTenno library."""

__all__ = ["VALID_LANGUAGES", "MAIN_ROOT", "API_ROOT", "ASSET_ROOT"]

from typing import Final, Literal

MAIN_ROOT: Final[str] = "https://warframe.market"
API_ROOT: Final[str] = "https://api.warframe.market/v1"
ASSET_ROOT: Final[str] = "https://warframe.market/static/assets"

VALID_LANGUAGES = Literal[
    "en",
    "ru",
    "ko",
    "fr",
    "sv",
    "de",
    "zh_hans",
    "zh_hant",
    "pt",
    "es",
    "pl",
]

VALID_TRANSLATIONS_RAW = {
    "en",
    "ru",
    "ko",
    "fr",
    "sv",
    "de",
    "zh_hans",
    "zh_hant",
    "pt",
    "es",
    "pl",
}
