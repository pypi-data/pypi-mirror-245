"""Module holding the Misc. interface class."""

from typing import Optional

from .._backends.misc import MiscBackend
from ..constants import VALID_LANGUAGES
from ..models.locations import Location
from ..models.missions import DroptableNPC, PartialMission


class Misc(MiscBackend):
    """Class for the misc backends."""

    async def get_locations(
        self, language: Optional[VALID_LANGUAGES] = None
    ) -> list[Location]:
        """Gets a list of all locations.

        Parameters
        ----------
        language : Optional[VALID_LANGUAGES]
            The language of the locations. Default: ``None``, meaning the default set during client construction.

        Returns
        -------
        list[Location]

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     locations = await pytenno.misc.get_locations()
        >>>     for location in locations:
        >>>         print(location.node_name)
        """
        return await self._get_locations(language)

    async def get_npcs(
        self, language: Optional[VALID_LANGUAGES] = None
    ) -> list[DroptableNPC]:
        """Gets a list of all NPCs.

        Parameters
        ----------
        language : Optional[VALID_LANGUAGES]
            The language of the NPCs. Default: ``None``, meaning the default set during client construction.

        Returns
        -------
        list[NPC]

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     npcs = await pytenno.misc.get_npcs()
        >>>     for npc in npcs:
        >>>         print(npc.name)
        """
        return await self._get_npcs(language)

    async def get_missions(
        self, language: Optional[VALID_LANGUAGES] = None
    ) -> list[PartialMission]:
        """Gets a list of all missions.

        Parameters
        ----------
        language : Optional[VALID_LANGUAGES]
            The language of the missions. Default: ``None``, meaning the default set during client construction.

        Returns
        -------
        list[PartialMission]

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     missions = await pytenno.misc.get_missions()
        >>>     for mission in missions:
        >>>         print(mission.name)
        """
        return await self._get_missions(language)
