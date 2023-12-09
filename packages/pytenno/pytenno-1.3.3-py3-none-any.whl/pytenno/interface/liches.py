"""Module holding the Liches interface class."""

from typing import Optional

from .._backends.liches import LichesBackend
from ..constants import VALID_LANGUAGES
from ..models.liches import LichEphemera, LichQuirk, LichWeapon


class Liches(LichesBackend):
    """Class for the liches backend."""

    async def get_weapons(
        self, language: Optional[VALID_LANGUAGES] = None
    ) -> list[LichWeapon]:
        """Gets all weapons.

        Parameters
        ----------
        language : Optional[VALID_LANGUAGES]
            The language of the weapons. Default: ``None``, meaning the default set during client construction.

        Returns
        -------
        list[LichWeapon]

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     weapons = await pytenno.liches.get_weapons()
        >>>     for weapon in weapons:
        >>>         print(weapon.url_name)
        """
        return await self._get_weapons(language)

    async def get_ephemeras(
        self, language: Optional[VALID_LANGUAGES] = None
    ) -> list[LichEphemera]:
        """Gets all lich ephemeras.

        Parameters
        ----------
        language : Optional[VALID_LANGUAGES]
            The language of the ephemeras. Default: ``None``, meaning the default set during client construction.

        Returns
        -------
        list[LichEphemera]

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     ephemeras = await pytenno.liches.get_ephemeras()
        >>>     for ephemera in ephemeras:
        >>>         print(ephemera.url_name)
        """
        return await self._get_ephemeras(language)

    async def get_quirks(
        self, language: Optional[VALID_LANGUAGES] = None
    ) -> list[LichQuirk]:
        """Gets all lich quirks.

        Parameters
        ----------
        language : Optional[VALID_LANGUAGES]
            The language of the quirks. Default: ``None``, meaning the default set during client construction.

        Returns
        -------
        list[LichQuirk]

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     quirks = await pytenno.liches.get_quirks()
        >>>     for quirk in quirks:
        >>>         print(quirk.url_name)
        """
        return await self._get_quirks(language)
