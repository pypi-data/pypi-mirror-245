"""Module holding the AuctionEntries interface class."""

from .._backends.auction_entries import AuctionEntriesBackend
from ..models.auctions import AuctionEntryExpanded


class AuctionEntries(AuctionEntriesBackend):
    """The AuctionEntries interface class."""

    def __init__(self, backend: AuctionEntriesBackend) -> None:
        """Initializes the interface class. For internal use."""
        super().__init__(backend)

    async def get_by_id(self, auction_id: str) -> AuctionEntryExpanded:
        """Gets a specific auction entry by ID.

        Parameters
        ----------
        auction_id : str
            The ID of the auction entry to get.

        Returns
        -------
        AuctionEntryExpanded

        Example
        -------
        >>> async with PyTenno() as tenno:
        >>>     auction = await tenno.AuctionEntries.get_by_id("...")
        >>>     print(auction.owner.ingame_name, auction.platinum)
        """
        return await self._get_by_id(auction_id)

    async def get_bids_by_id(self, auction_id: str) -> AuctionEntryExpanded:
        """Gets all bids for a specific auction entry by ID.

        Parameters
        ----------
        auction_id : str
            The ID of the auction entry to get bids for.

        Returns
        -------
        AuctionEntryExpanded

        Example
        -------
        >>> async with PyTenno() as tenno:
        >>>     auction = await tenno.AuctionEntries.get_bids_by_id("...")
        >>>     print(auction.owner.ingame_name, auction.platinum)
        """
        return await self._get_bids_by_id(auction_id)
