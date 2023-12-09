from ..models.droptable import DroptableNPC
from ..models.locations import Location
from ..models.missions import PartialMission
from ..utils import _from_data
from .core import BackendAdapter


class MiscBackend(BackendAdapter):
    async def _get_locations(self, language):
        url = "/misc/locations"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        return [_from_data(Location, node) for node in response["payload"]["locations"]]

    async def _get_npcs(self, language):
        url = "/misc/npc"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        return [_from_data(DroptableNPC, node) for node in response["payload"]["npc"]]

    async def _get_missions(self, language):
        url = "/misc/missions"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        return [
            _from_data(PartialMission, node) for node in response["payload"]["missions"]
        ]
