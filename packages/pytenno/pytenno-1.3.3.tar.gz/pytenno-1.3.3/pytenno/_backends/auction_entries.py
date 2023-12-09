from ..models.auctions import AuctionEntryExpanded
from ..utils import _from_data
from .core import BackendAdapter


class AuctionEntriesBackend(BackendAdapter):
    async def _get_by_id(
        self,
        auction_id: str,
    ):
        data = await self._backend._request(f"/auctions/entry/{auction_id}")
        return _from_data(AuctionEntryExpanded, data)

    async def _get_bids_by_id(self, auction_id: str):
        data = await self._backend._request(f"/auctions/entry/{auction_id}/bids")
        return _from_data(AuctionEntryExpanded, data)
