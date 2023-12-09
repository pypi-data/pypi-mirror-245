from typing import Literal, Union

from ..models.auctions import (AuctionEntry, AuctionEntryExpanded,
                               KubrowAuction, LichAuction, RivenAuction)
from ..models.enums import Element, Platform, Polarity
from ..utils import format_name, _from_data
from .core import BackendAdapter


class AuctionsBackend(BackendAdapter):
    async def _create_auction(
        self,
        item: Union[RivenAuction, LichAuction, KubrowAuction],
        note: str,
        starting_price: int,
        buyout_price: int,
        minimal_reputation: int = 0,
        minimal_increment: int = 1,
        private: bool = False,
    ):
        url = "/auctions/create"
        attributes = [
            {
                [
                    {
                        "positive": attribute.positive,
                        "value": attribute.value,
                        "url": attribute.url_name,
                    }
                ]
                for attribute in item.attributes
            }
        ]
        data = {
            "note": note,
            "starting_price": starting_price,
            "buyout_price": buyout_price,
            "minimal_reputation": minimal_reputation,
            "minimal_increment": minimal_increment,
            "private": private,
            "item": {
                "type": item.type.name.lower(),
                "attributes": attributes,
                "name": item.name.lower(),
                "mastery_level": item.mastery_level,
                "re_rolls": item.re_rolls,
                "weapon_url_name": item.weapon_url_name,
                "polarity": item.polarity.name.lower(),
                "mod_rank": item.mod_rank,
            },
        }

        response = await self._backend._request(url, method="post", data=str(data))
        return _from_data(AuctionEntry, response["payload"]["auction"])

    async def _find_riven_auctions(
        self,
        *,
        weapon_url_name: str,
        platform: Platform,
        buyout_policy: Literal["with", "direct"] | None = None,
        mastery_rank_min: int | None = None,
        mastery_rank_max: int | None = None,
        re_rolls_min: int | None = None,
        re_rolls_max: int | None = None,
        positive_stats: list[str] | None = None,
        negative_stats: list[str] | None = None,
        polarity: Polarity = Polarity.any,
        mod_rank: Literal["any", "maxed"] | None = None,
        sort_by: Literal[
            "price_desc", "price_asc", "positive_attr_desc", "positive_attr_asc"
        ]
        | None = None,
        operation: Literal["anyOf", "allOf"] | None = None,
    ):
        url = (
            f"/auctions/search?type=riven&"
            + (
                f"weapon_url_name={weapon_url_name}&"
                if weapon_url_name is not None
                else ""
            )
            + (
                f"mastery_rank_min={mastery_rank_min}&"
                if mastery_rank_min is not None
                else ""
            )
            + (
                f"mastery_rank_max={mastery_rank_max}&"
                if mastery_rank_max is not None
                else ""
            )
            + (f"re_rolls_min={re_rolls_min}&" if re_rolls_min is not None else "")
            + (f"re_rolls_max={re_rolls_max}&" if re_rolls_max is not None else "")
            + (
                f"positive_stats={','.join([str(s) for s in positive_stats])}&"
                if positive_stats is not None
                else ""
            )
            + (
                f"negative_stats={','.join([str(s) for s in negative_stats])}&"
                if negative_stats is not None
                else ""
            )
            + f"polarity={polarity}&"
            + (f"mod_rank={mod_rank}&" if mod_rank is not None else "")
            + (f"sort_by={sort_by}&" if sort_by is not None else "")
            + (f"operation={operation}&" if operation is not None else "")
            + (f"buyout_policy={buyout_policy}" if buyout_policy is not None else "")
        ).strip("&")

        headers = {"Platform": platform.name.lower()}
        response = await self._backend._request(url, headers=headers)

        return [
            _from_data(AuctionEntryExpanded, node)
            for node in response["payload"]["auctions"]
        ]

    async def _find_lich_auctions(
        self,
        *,
        platform: Platform,
        weapon_url_name: str,
        element: Element,
        ephemera: bool,
        damage_min: int,
        damage_max: int,
        quirk_url_name: str,
        sort_by: Literal[
            "price_desc", "price_asc", "positive_attr_desc", "positive_attr_asc"
        ] = "price_desc",
        buyout_policy: Literal["with", "direct", "all"] = "all",
    ):
        url = (
            f"/auctions/search?type=lich&"
            + f"weapon_url_name={format_name(weapon_url_name)}&"
            + (f"element={element.name.lower()}&" if element is not None else "")
            + (f"ephemera={ephemera}&" if ephemera is not None else "")
            + (f"damage_min={damage_min}&" if damage_min is not None else "")
            + (f"damage_max={damage_max}&" if damage_max is not None else "")
            + (f"quirk={quirk_url_name}&" if quirk_url_name is not None else "")
            + (f"sort_by={sort_by}&" if sort_by is not None else "")
            + (f"buyout_policy={buyout_policy}" if buyout_policy is not None else "")
        ).strip("&")
        headers = {"Platform": platform.name.lower()}
        response = await self._backend._request(url, headers=headers)

        return [
            _from_data(AuctionEntryExpanded, node)
            for node in response["payload"]["auctions"]
        ]
