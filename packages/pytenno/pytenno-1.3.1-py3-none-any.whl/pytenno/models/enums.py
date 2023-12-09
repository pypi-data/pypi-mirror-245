from enum import Enum


class Base(Enum):
    """
    Base class for all enums.
    :meta private:
    """

    def __int__(self):
        return self.value

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)


class RelicQuality(Base):
    """Represents the quality of a relic.

    Attributes
    ----------
    intact : int
        The quality of an intact relic.
    exceptional : int
        The quality of an exceptional relic.
    flawless : int
        The quality of a flawless relic.
    radiant : int
        The quality of a radiant relic.
    """

    intact = 0
    exceptional = 1
    flawless = 2
    radiant = 3


class FishSize(Base):
    """Represents the size of a fish.

    Attributes
    ----------
    small : int
        The size of a small fish.
    medium : int
        The size of a medium fish.
    large : int
        The size of a large fish.
    """

    small = 0
    medium = 1
    large = 2


class FortunaFishQuality(Base):
    """Represents the quality of a fish in fortuna

    Attributes
    ----------
    basic : int
        The quality of a basic fish.
    adorned : int
        The quality of an adorned fish.
    magnificent : int
        The quality of a magnificent fish.
    """

    basic = 0
    adorned = 1
    magnificent = 2


class Subtype(Base):
    """Represents the subtype of an item. Basically a combination of ``RelicQuality``, ``FishSize`` and ``FortunaFishQuality``.

    Attributes
    ----------
    intact : int
        The subtype of an intact relic.
    exceptional : int
        The subtype of an exceptional relic.
    flawless : int
        The subtype of a flawless relic.
    radiant : int
        The subtype of a radiant relic.
    small : int
        The subtype of a small fish.
    medium : int
        The subtype of a medium fish.
    large : int
        The subtype of a large fish.
    basic : int
        The subtype of a basic fortuna fish.
    adorned : int
        The subtype of an adorned fortuna fish.
    magnificent : int
        The subtype of a magnificent fortuna fish.
    """

    intact = 0
    exceptional = 1
    flawless = 2
    radiant = 3
    small = 4
    medium = 5
    large = 5
    basic = 6
    adorned = 7
    magnificent = 8


class ItemRarity(Base):
    """Represents the rarity of an item.

    Attributes
    ----------
    very_common : int
        The rarity of a very common item.
    common : int
        The rarity of a common item.
    uncommon : int
        The rarity of an uncommon item.
    rare : int
        The rarity of a rare item.
    legendary : int
        The rarity of a legendary item.
    peculiar : int
        The rarity of a peculiar item.
    """

    very_common = 0
    common = 1
    uncommon = 2
    rare = 3
    legendary = 4
    peculiar = 5


class OrderType(Base):
    """Represents the type of an order.

    Attributes
    ----------
    buy : int
        The order is buying the item(s).
    sell : int
        The order is selling the item(s).
    """

    buy = 0
    sell = 1


class MeasurementUnit(Base):
    """Represents the measurement unit, for riven attributes.

    Attributes
    ----------
    seconds : int
        The measurement unit is seconds.
    percent : int
        The measurement unit is percent.
    """

    seconds = 0
    percent = 1


class Element(Base):
    """Represents the element of a weapon, ephemera, or lich weapon.

    Attributes
    ----------
    impact : int
        The element is impact.
    heat : int
        The element is heat.
    cold : int
        The element is cold.
    electricity : int
        The element is electricity.
    toxin : int
        The element is toxin.
    magnetic : int
        The element is magnetic.
    radiation : int
        The element is radiation.

    Notes
    -----
    This does **not** include combined elements, aka. ``.heat`` + ``.cold`` -> ``blast``.
    """

    impact = 0
    heat = 1
    cold = 2
    electricity = 3
    toxin = 4
    magnetic = 5
    radiation = 6


class PatreonBadge(Base):
    """Represents the patreon badge of a user.

    Attributes
    ----------
    bronze : int
        The badge is bronze.
    silver : int
        The badge is silver.
    gold : int
        The badge is gold.
    platinum : int
        The badge is platinum.
    """

    bronze = 0
    silver = 1
    gold = 2
    platinum = 3


class Platform(Base):
    """Represents the platform of a user, order, or auction.

    Attributes
    ----------
    ps4 : int
        The platform is on PlayStation 4.
    pc : int
        The platform is on PC.
    xbox : int
        The platform is on Xbox.
    switch : int
        The platform is on Nintendo Switch.
    """

    ps4 = 0
    pc = 1
    xbox = 2
    switch = 3


class UserRole(Base):
    """Represents the role of a user.

    Attributes
    ----------
    anonymous : int
        The user is an anonymous user.
    user : int
        The user is a regular user.
    moderator : int
        The user is a moderator.
    admin : int
        The user is an admin.
    """

    anonymous = 0
    user = 1
    moderator = 2
    admin = 3


class UserStatus(Base):
    """Represents the status of a user.

    Attributes
    ----------
    offline : int
        The user is offline.
    online : int
        The user is online.
    ingame : int
        The user is in Warframe.
    """

    offline = 0
    online = 1
    ingame = 2


class RivenWeaponGroup(Base):
    """Represents group of weapon a riven is on.

    Attributes
    ----------
    primary : int
        The riven is on a primary weapon.
    secondary : int
        The riven is on a secondary weapon.
    melee : int
        The riven is on a melee weapon.
    zaw : int
        The riven is on a zaw.
    sentinel : int
        The riven is on a sentinel weapon.
    archgun : int
        The riven is on an arch gun.
    kitgun : int
        The riven is on a kit gun.
    """

    primary = 0
    secondary = 1
    melee = 2
    zaw = 3
    sentinel = 4
    archgun = 5
    kitgun = 6


class RivenAttributeGroup(Base):
    """Represents the group of an riven attribute. Used for grouping UI elements.

    Attributes
    ----------
    default : int
        The attribute is in the default group.
    melee : int
        The attribute is in the melee group.
    top : int
        The attribute is at the top of the group.
    """

    default = 0
    melee = 1
    top = 2


class RivenWeaponType(Base):
    """Represents the type of the weapon a riven is on.

    Attributes
    ----------
    rifle : int
        The riven in on a rifle-class weapon.
    shotgun : int
        The riven in on a shotgun-class weapon.
    pistol : int
        The riven in on a pistol-class weapon.
    melee : int
        The riven in on a melee-class weapon.
    zaw : int
        The riven in on a zaw-class weapon.
    kitgun : int
        The riven in on a kitgun-class weapon.
    """

    rifle = 0
    shotgun = 1
    pistol = 2
    melee = 3
    zaw = 4
    kitgun = 5


class Polarity(Base):
    """Represents the polarity of a mod.

    Attributes
    ----------
    madurai : int
        The mod is madurai.
    vazarin : int
        The mod is vazarin.
    naramon : int
        The mod is naramon.
    zanurik : int
        The mod is zanurik.
    any : int
        The mod is any polarity. Used in some search scenarios.
    """

    madurai = 0
    vazarin = 1
    naramon = 2
    zanurik = 3
    any = 4
    kitgun = 5


class TranslationLanguage(Base):
    """Represents the language of a translation.

    Attributes
    ----------
    en : int
        The translation is in English.
    ru : int
        The translation is in Russian.
    ko : int
        The translation is in Korean.
    fr : int
        The translation is in French.
    sv : int
        The translation is in Swedish.
    de : int
        The translation is in German.
    zh_hant : int
        The translation is in Chinese (Traditional).
    zh_hans : int
        The translation is in Chinese (Simplified).
    pt : int
        The translation is in Portuguese.
    es : int
        The translation is in Spanish.
    pl : int
        The translation is in Polish.
    """

    en = 0
    ru = 1
    ko = 2
    fr = 3
    sv = 4
    de = 5
    zh_hant = 6
    zh_hans = 7
    pt = 8
    es = 9
    pl = 10


class IconFormat(Base):
    """Represents the format of an icon.

    Attributes
    ----------
    land : int
        The icon is in landscape format.
    port : int
        The icon is in portrait format.
    """

    land = 0
    port = 1


class AnimationFormat(Base):
    """Represents the format of an animation.

    Attributes
    ----------
    land : int
        The animation is in landscape format.
    port : int
        The animation is in portrait format.
    """

    land = 0
    port = 1


class AuctionType(Base):
    """Represents the type of an auction.

    Attributes
    ----------
    riven : int
        The auction is for a riven.
    lich : int
        The auction is for a lich.
    kubrow : int
        The auction is for a kubrow.
    """

    riven = 0
    lich = 1
    kubrow = 2


class AuctionMarking(Base):
    """Represents the marking of an auction.

    Attributes
    ----------
    removing : int
        The auction is marked for removal.
    archiving : int
        The auction is marked for archiving.
    """

    removing = 0
    archiving = 1


class Rotation(Base):
    """Represents the rotation of a stage.

    Attributes
    ----------
    a : int
        The stage is in rotation A.
    b : int
        The stage is in rotation B.
    c : int
        The stage is in rotation C.
    """

    a = 0
    b = 1
    c = 2


class Stage(Base):
    """Represents the stage of a mission.

    Attributes
    ----------
    _1 : int
        The stage is 1.
    _2 : int
        The stage is 2.
    _3 : int
        The stage is 3.
    _4 : int
        The stage is 4.
    final : int
        The stage is the final stage.
    """

    _1 = 0
    _2 = 1
    _3 = 2
    _4 = 3
    final = 4


class Faction(Base):
    """Represents the faction of a mission node.

    Attributes
    ----------
    infested : int
        The node is controlled by the Infested.
    grineer : int
        The node is controlled by the Grineer.
    corpus : int
        The node is controlled by the Corpus.
    corrupted : int
        The node is controlled by the Corrupted.
    """

    infested = 0
    grineer = 1
    corpus = 2
    corrupted = 3


class RivenStat(Base):
    """Represents the stat of a riven attribute.

    Notes
    -----
    The stat names do not always line up with the actual names in Warframe.

    Some names, such as ``.fire_rate_attack_speed``, are modified
    versions of the names in the API, due to limitations of Python.
    Calling the ``.__str__`` method will return the actual name.
    """

    ammo_maximum = 0
    """The stat modifies the maximum ammo of the weapon the riven is on."""
    cold = 1
    """The stat modifies the ``Element.cold`` damage of the weapon the riven is on."""
    critical_chance = 2
    """The stat modifies the critical chance damage of the weapon the riven is on."""
    damage = 3
    """The stat modifies the base damage of the weapon the riven is on."""
    damage_vs_corpus = 4
    """The stat modifies the damage of the weapon the riven is on against the Corpus."""
    damage_vs_grineer = 5
    """The stat modifies the damage of the weapon the riven is on against the Corpus."""
    damage_vs_infested = 6
    """The stat modifies the damage of the weapon the riven is on against the faction."""
    electricity = 7
    """The stat modifies the ``Element.electricity`` damage of the weapon the riven is on."""
    fire_rate_attack_speed = 8
    """The stat modifies the fire rate / attack speed of the weapon the riven is on."""
    heat = 9
    """The stat modifies the ``Element.heat`` damage of the weapon the riven is on."""
    impact = 10
    """The stat modifies the ``Element.impact`` damage of the weapon the riven is on."""
    magazine_capacity = 11
    """The stat modifies the magazine capacity of the weapon the riven is on."""
    multishot = 12
    """The stat modifies the multishot of the weapon the riven is on."""
    projectile_speed = 13
    """The stat modifies the projectile speed of the weapon the riven is on."""
    punch_through = 14
    """The stat modifies the punch through of the weapon the riven is on."""
    puncture = 15
    """The stat modifies the ``Element.puncture`` damage of the weapon the riven is on."""
    reload_speed = 16
    """The stat modifies the reload speed of the weapon the riven is on."""
    slash = 17
    """The stat modifies the ``Element.slash`` damage of the weapon the riven is on."""
    status_chance = 18
    """The stat modifies the status chance of the weapon the riven is on."""
    status_duration = 19
    """The stat modifies the status duration of the weapon the riven is on."""
    toxin = 20
    """The stat modifies the ``Element.toxin`` damage of the weapon the riven is on."""
    weapon_recoil = 21
    """The stat modifies the weapon recoil of the weapon the riven is on."""
    initial_combo = 22
    """The stat modifies the initial combo of the weapon the riven is on."""
    range = 23
    """The stat modifies the range of the weapon the riven is on."""
    chance_to_gain_extra_combo_count = 24
    """The stat modifies the chance for the weapon to gain an extra combo count on a hit."""
    combo_duration = 25
    """The stat modifies the duration of the combo of the weapon the riven is on."""
    critical_chance_on_slide_attack = 26
    """The stat modifies the critical chance on a slide attack of the weapon the riven is on."""
    finisher_damage = 27
    """The stat modifies the finisher damage of the weapon the riven is on."""
    channeling_efficiency = 28
    """The stat modifies the channeling efficiency (heavy attack efficiency) of the weapon the riven is on."""
    channeling_damage = 29
    """The stat modifies the channeling damage (heavy attack damage) of the weapon the riven is on."""

    def __str__(self):
        # Some of these values have non-python-friendly names
        if self.value == 3:
            return "base_damage_/_melee_damage"
        elif self.value == 8:
            return "fire_rate_/_attack_speed"
        return self.name


class DropSourceType(Base):
    """Represents the type of drop source.

    Attributes
    ----------
    relic: int
        The source of the drop was a relic.
    """

    relic = 0
    mission = 1