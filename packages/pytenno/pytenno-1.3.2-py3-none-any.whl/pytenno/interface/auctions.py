"""Module holding the Auctions interface class."""

from typing import Literal, Optional, Union

from .._backends.auctions import AuctionsBackend
from ..models.auctions import (AuctionEntryExpanded, KubrowAuction,
                               LichAuction, RivenAuction)
from ..models.enums import Element, Platform, Polarity, RivenStat


class Auctions(AuctionsBackend):
    """A class for creating and searching for auctions with certain criteria."""

    async def create_auction(
        self,
        item: Union[RivenAuction, LichAuction, KubrowAuction],
        note: str,
        starting_price: int,
        buyout_price: int,
        minimal_reputation: Optional[int] = 0,
        minimal_increment: Optional[int] = 1,
        private: Optional[bool] = False,
    ) -> list[AuctionEntryExpanded]:
        """Creates a new auction.

        Parameters
        ----------
        item : RivenAuction, LichAuction, KubrowAuction
            The item to auction.
        note : str
            The note to put on the auction.
        starting_price : int
            The starting price of the auction. (In platinum)
        buyout_price : int
            The buyout price of the auction. (In platinum)
        minimal_reputation : int, optional
            The minimmum reputation a user must have to bid on the auction.
        minimal_increment : int, optional
            The minimum amount between bids. (In platinum)
        private : bool, optional
            Whether the auction is private or not. If it is private, you can set it to public in the auction settings in the web interface.

        Returns
        -------
        list[AuctionEntryExpanded]

        Raises
        ------
        ValueError
            If the starting price is higher than the buyout price.
        ValueError
            If the minimal increment is less than 1.

        Example
        -------
        >>> async with PyTenno() as tenno:
        >>>     auction = await tenno.Auctions.create_auction(
        >>>         item=RivenAuction(...),
        >>>         note="...",
        >>>         starting_price=100,
        >>>         buyout_price=200,
        >>>         minimal_reputation=0,
        >>>         minimal_increment=50
        >>>     )
        >>>     print(auction.owner.ingame_name, auction.platinum)
        """
        if starting_price > buyout_price:
            raise ValueError("Starting price cannot be higher than buyout price.")
        if minimal_increment < 1:
            raise ValueError("Minimal increment cannot be less than 1.")

        return await self._create_auction(
            item,
            note,
            starting_price,
            buyout_price,
            minimal_reputation,
            minimal_increment,
            private,
        )

    async def find_riven_auctions(
        self,
        *,
        weapon_url_name: str,
        platform: Platform = None,
        mastery_rank_min: int = None,
        mastery_rank_max: int = None,
        re_rolls_min: int = None,
        re_rolls_max: int = None,
        positive_stats: list[RivenStat] = None,
        negative_stats: list[RivenStat] = None,
        polarity: Polarity = Polarity.any,
        mod_rank: Literal["any", "maxed"] = None,
        sort_by: Optional[
            Literal[
                "price_desc", "price_asc", "positive_attr_desc", "positive_attr_asc"
            ]
        ] = None,
        operation: Optional[Literal["anyOf", "allOf"]] = None,
        buyout_policy: Optional[Literal["with", "direct"]] = None,
    ) -> list[AuctionEntryExpanded]:
        """Finds all riven auctions that match the given criteria.

        Parameters
        ----------
        weapon_url_name : str
            The URL name of the weapon to search for.
        platform : Platform, optional
            The platform to search for riven auctions on. Default: ``None``, meaning the default set when the client was created.
        mastery_rank_min : int, optional
            The minimum mastery rank of the riven. Default: None.
        mastery_rank_max : int, optional
            The maximum mastery rank of the riven. Default: None.
        re_rolls_min : int, optional
            The minimum number of re-rolls of the riven. Default: None.
        re_rolls_max : int, optional
            The maximum number of re-rolls of the riven. Default: None.
        positive_stats : list[RivenStat], optional
            Restricts the riven to have the given positive stats. Maximum amount is 3. Default: None.
        negative_stats : list[RivenStat], optional
            Restricts the riven to have the given negative stats. Maximum amount is 3. Default: None.
        polarity : Polarity, optional
            The polarity of the riven. Default: ``Polarity.any``.

        Returns
        -------
        list[AuctionEntryExpanded]

        Raises
        ------
        ValueError
            If the amount of ``positive_stats`` is greater than 3.
        ValueError
            If the amount of ``negative_stats`` is greater than 3.
        ValueError
            If the ``mastery_rank_min`` is greater than the ``mastery_rank_max``.
        ValueError
            If the ``re_rolls_min`` is greater than the ``re_rolls_max``.
        ValueError
            If the ``mastery_rank_min`` is less than 0.
        ValueError
            If the ``re_rolls_min`` is less than 0.

        Example
        -------
        >>> auctions = await tenno.auctions.find_riven_auctions(
        >>>     weapon_url_name="shedu",
        >>>     mastery_rank_max=9,
        >>>     re_rolls_max=10
        >>> )
        >>> for auction in auctions:
        >>>     print(auction.id)
        >>>     print(auction.item.element.name)
        """
        if positive_stats is not None and len(positive_stats) > 3:
            raise ValueError("The amount of positive stats cannot be greater than 3.")
        if negative_stats is not None and len(negative_stats) > 3:
            raise ValueError("The amount of negative stats cannot be greater than 3.")
        if mastery_rank_min is not None and mastery_rank_min > mastery_rank_max:
            raise ValueError(
                "The mastery rank min cannot be greater than the mastery rank max."
            )
        if re_rolls_min is not None and re_rolls_min > re_rolls_max:
            raise ValueError(
                "The re-rolls min cannot be greater than the re-rolls max."
            )
        if mastery_rank_min is not None and mastery_rank_min < 0:
            raise ValueError("The mastery rank min cannot be less than 0.")
        if re_rolls_min is not None and re_rolls_min < 0:
            raise ValueError("The re-rolls min cannot be less than 0.")

        return await self._find_riven_auctions(
            platform=platform,
            weapon_url_name=weapon_url_name,
            mastery_rank_min=mastery_rank_min,
            mastery_rank_max=mastery_rank_max,
            re_rolls_min=re_rolls_min,
            re_rolls_max=re_rolls_max,
            positive_stats=positive_stats,
            negative_stats=negative_stats,
            polarity=polarity,
            mod_rank=mod_rank,
            sort_by=sort_by,
            operation=operation,
            buyout_policy=buyout_policy,
        )

    async def find_lich_auctions(
        self,
        *,
        weapon_url_name: str,
        platform: Platform = None,
        element: Optional[Element] = None,
        ephemera: Optional[bool] = None,
        damage_min: Optional[int] = None,
        damage_max: Optional[int] = None,
        quirk_url_name: Optional[str] = None,
        sort_by: Optional[
            Literal[
                "price_desc", "price_asc", "positive_attr_desc", "positive_attr_asc"
            ]
        ] = "price_desc",
        buyout_policy: Optional[Literal["with", "direct"]] = None,
    ) -> list[AuctionEntryExpanded]:
        """Finds all lich auctions that match the given criteria.

        Parameters
        ----------
        weapon_url_name : str
            The URL name of the weapon to search for.
        platform : Platform
            The platform to search for lich auctions on. Default: ``None``, meaning the default set when the client was created.
        element : Element
            The element of the lich. Default: None.
        ephemera : bool
            Whether the lich is ephemeral. Default: None.
        damage_min : int
            The minimum damage of the lich. Default: None.
        damage_max : int
            The maximum damage of the lich. Default: None.
        quirk_url_name : str
            The URL name of the quirk of the lich. Default: None.
        sort_by : Literal
            The sort order of the results. Default: `"price_desc"`.
        buyout_policy : Literal
            The buyout policy of the results. Default: None.

        Returns
        -------
        list[AuctionEntryExpanded]

        Raises
        ------
        ValueError
            If the damage min is greater than the damage max.
        ValueError
            If the damage min is less than 0.
        ValueError
            If the damage max is less than 0.

        Example
        -------
        >>> async with PyTenno() as tenno:
        >>>     auctions = await tenno.auctions.find_lich_auctions(
        >>>         weapon_url_name="kuva_bramma",
        >>>         damage_min=20,
        >>>         element=Element.toxin,
        >>>     )
        >>>     for auction in auctions:
        >>>         print(auction.id, auction.owner.ingame_name)
        """
        if damage_min is not None and damage_min > damage_max:
            raise ValueError("The damage min cannot be greater than the damage max.")
        if damage_min is not None and damage_min < 0:
            raise ValueError("The damage min cannot be less than 0.")
        if damage_max is not None and damage_max < 0:
            raise ValueError("The damage max cannot be less than 0.")

        return await self._find_lich_auctions(
            platform=str(platform),
            weapon_url_name=weapon_url_name,
            element=element,
            ephemera=ephemera,
            damage_min=damage_min,
            damage_max=damage_max,
            quirk_url_name=quirk_url_name,
            sort_by=sort_by,
            buyout_policy=buyout_policy,
        )
