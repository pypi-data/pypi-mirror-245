"""Module containg models for items."""

from dataclasses import dataclass

from pytenno.constants import VALID_TRANSLATIONS_RAW
from pytenno.utils import _from_data

from .droptable import Drop
from .enums import IconFormat, ItemRarity, Subtype


@dataclass
class LangInItem:
    """Represents an item's localized data."""

    item_name: str
    """The translated name of the item."""
    description: str
    """The translated description of the item."""
    wiki_link: str | None
    """The link to the wiki page of the item."""
    drop: list[Drop]
    """Where the item can be found."""

    def _from_data(data: dict):
        data["drop"] = [Drop(**drop) for drop in data["drop"]]
        return LangInItem(**data)


@dataclass(kw_only=True)
class ItemCommon:
    """Common base class that an item can inherit from."""

    id: str
    """The ID of the item."""
    url_name: str
    """The URL name of the item."""
    icon: str
    """The URL of the item's icon."""
    icon_format: IconFormat | None = None
    """The format of the item's icon."""
    sub_icon: str = None
    """The URL of the item's sub icon. For example if the item is part of a set, `icon` will the icon of the set, while `sub_icon` will be the icon of the item in the set."""
    thumb: str
    """The URL of the item's thumbnail."""
    tags: list[str]
    """The tags of the item."""
    mod_max_rank: int | None = None
    """The maximum rank of the item."""
    subtypes: list[Subtype] | None = None
    """The subtypes of the item."""
    cyan_stars: int | None = None
    """The number of cyan stars the item has."""
    amber_stars: int | None = None
    """The number of amber stars the item has."""
    ducats: int | None = None
    """The ducat worth of the item."""

    def __repr__(self):
        return f"<ItemCommon id={self.id} url_name={self.url_name} tags={self.tags}>"


@dataclass(kw_only=True)
class TranslatedItemName:
    """Represents an item's localized name."""

    item_name: str
    """The translated name of the item."""


@dataclass(kw_only=True)
class ItemInOrder(ItemCommon):
    """Represents an item in an order."""

    en: TranslatedItemName
    """The English name of the item."""
    ru: TranslatedItemName
    """The Russian name of the item."""
    ko: TranslatedItemName
    """The Korean name of the item."""
    fr: TranslatedItemName
    """The French name of the item."""
    de: TranslatedItemName
    """The German name of the item."""
    sv: TranslatedItemName
    """The Swedish name of the item."""
    zh_hant: TranslatedItemName
    """The Chinese (Traditional) name of the item."""
    zh_hans: TranslatedItemName
    """The Chinese (Simplified) name of the item."""
    pt: TranslatedItemName
    """The Portuguese name of the item."""
    es: TranslatedItemName
    """The Spanish name of the item."""
    pl: TranslatedItemName
    """The Polish name of the item."""

    def __repr__(self):
        return f"<ItemInOrder id={self.id} url_name={self.url_name} tags={self.tags}>"


@dataclass(kw_only=True)
class ItemFull(ItemInOrder):
    """same as ItemInOrder, but lang related fields contain more info, as well as ``rarity``, ``set_root``, ``mastery_level``, and ``trading_tax`` attributes."""

    set_root: bool
    """Whether the item is part of a set."""
    mastery_level: int
    """The mastery level of the item."""
    rarity: ItemRarity | None = None
    """The rarity of the item. If None, the item does not have any specific rarity."""
    trading_tax: int
    """The trading tax of the item."""
    quantity_for_set: int = None
    """The quantity of the item required to obtain the set."""

    en: LangInItem
    """The English translation of the item."""
    ru: LangInItem
    """The Russian translation of the item."""
    ko: LangInItem
    """The Korean translation of the item."""
    fr: LangInItem
    """The French translation of the item."""
    de: LangInItem
    """The German translation of the item."""
    sv: LangInItem
    """The Swedish translation of the item."""
    zh_hant: LangInItem
    """The Chinese (Traditional) translation of the item."""
    zh_hans: LangInItem
    """The Chinese (Simplified) translation of the item."""
    pt: LangInItem
    """The Portuguese translation of the item."""
    es: LangInItem
    """The Spanish translation of the item."""
    pl: LangInItem
    """The Polish translation of the item."""

    def _from_data(data: dict):
        for lang in (
            "en",
            "ru",
            "ko",
            "fr",
            "de",
            "sv",
            "zh_hant",
            "zh_hans",
            "pt",
            "es",
            "pl",
        ):
            data[lang] = LangInItem._from_data(data[lang])
        return _from_data(ItemFull, data, False)

    def __repr__(self):
        return f"<ItemFull id={self.id} url_name={self.url_name} tags={self.tags} rarity={self.rarity}>"


@dataclass
class ItemShort:
    """Represents a simplified version of an item."""

    id: str
    """The ID of the item."""
    url_name: str
    """The URL name of the item."""
    thumb: str
    """The URL of the item's thumbnail."""
    item_name: str
    """The name of the item."""
    vaulted: bool | None = None
    """Whether the item is vaulted. Default: `None`, meaning the item cannot be vaulted/unvaulted."""

    def __repr__(self):
        return f"<ItemShort id={self.id} url_name={self.url_name}>"
