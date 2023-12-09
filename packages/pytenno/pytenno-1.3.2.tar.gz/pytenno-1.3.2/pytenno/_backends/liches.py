from ..models.liches import LichEphemera, LichQuirk, LichWeapon
from ..utils import _from_data
from .core import BackendAdapter


class LichesBackend(BackendAdapter):
    async def _get_weapons(self, language):
        url = "/lich/weapons"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        return [_from_data(LichWeapon, node) for node in response["payload"]["weapons"]]

    async def _get_ephemeras(self, language):
        url = "/lich/ephemeras"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        return [
            _from_data(LichEphemera, node) for node in response["payload"]["ephemeras"]
        ]

    async def _get_quirks(self, language):
        url = "/lich/quirks"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        return [_from_data(LichQuirk, node) for node in response["payload"]["quirks"]]
