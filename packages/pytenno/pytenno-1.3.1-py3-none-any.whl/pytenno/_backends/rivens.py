from ..models.rivens import RivenAttribute, RivenItem
from ..utils import _from_data
from .core import BackendAdapter


class RivensBackend(BackendAdapter):
    async def _get_riven_items(self, language):
        url = "/riven/items"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        return [_from_data(RivenItem, node) for node in response["payload"]["items"]]

    async def _get_riven_attributes(self, language):
        url = "/riven/attributes"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        return [
            _from_data(RivenAttribute, node)
            for node in response["payload"]["attributes"]
        ]
