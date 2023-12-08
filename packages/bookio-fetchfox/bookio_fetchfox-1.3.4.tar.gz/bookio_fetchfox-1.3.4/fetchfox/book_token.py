from typing import Iterable, Tuple

from cachetools.func import ttl_cache

from fetchfox.apis import price
from fetchfox.apis.cardano import cexplorerio, dexhunterio
from fetchfox.constants.book import (
    BOOK_TOKEN_ASSET_ID,
    BOOK_TOKEN_ASSET_NAME,
    BOOK_TOKEN_POLICY_ID,
    BOOK_TOKEN_FINGERPRINT,
)
from fetchfox.constants.currencies import ADA, BOOK
from fetchfox.dtos import OrderDTO, OrderType, PairStatsDTO, StatsDTO


class BookToken:
    asset_id = BOOK_TOKEN_ASSET_ID
    asset_name = BOOK_TOKEN_ASSET_NAME
    fingerprint = BOOK_TOKEN_FINGERPRINT
    policy_id = BOOK_TOKEN_POLICY_ID
    symbol = BOOK

    def __init__(self, dexhunter_partner_code: str):
        self.dexhunter_partner_code = dexhunter_partner_code

    @property
    @ttl_cache(ttl=30)
    def ada(self) -> float:
        return dexhunterio.get_average_price(
            self.asset_id,
            partner_code=self.dexhunter_partner_code,
        )

    @property
    @ttl_cache(ttl=30)
    def usd(self) -> float:
        return price.usd(ADA) * self.ada

    @property
    def cardanoscan_url(self):
        return "https://cardanoscan.io/token/{asset_id}".format(
            asset_id=self.asset_id,
        )

    @property
    def cexplorer_url(self):
        return "https://cexplorer.io/asset/{fingerprint}".format(
            fingerprint=self.fingerprint,
        )

    @property
    def minswap_url(self):
        return "https://app.minswap.org/swap?currencySymbolA={policy_id}&tokenNameA={token_name}&currencySymbolB=&tokenNameB=".format(
            policy_id=self.policy_id,
            token_name=self.asset_name,
        )

    @property
    def owners(self) -> Tuple[int, int]:
        tx = cexplorerio.get_asset_detail(self.fingerprint)

        return tx["epoch"], tx["owners_acc"]

    @property
    def pair_stats(self) -> PairStatsDTO:
        stats = dexhunterio.get_pair_stats(
            self.asset_id,
            partner_code=self.dexhunter_partner_code,
        )

        stats_dto = StatsDTO(
            ada=stats["token2Amount"],
            book=stats["token1Amount"],
            daily_txs=stats["dailyTxAmount"],
            daily_buys=stats["dailyBuysCount"],
            daily_sales=stats["dailySalesCount"],
            daily_volume=stats["dailyVolume"],
            price_change_hour=stats["priceChangeHour"],
            price_change_day=stats["priceChangeDay"],
            price_change_week=stats["priceChangeWeek"],
            price_change_month=stats["priceChangeMonth"],
        )

        pair_stats_dto = PairStatsDTO(stats_dto)

        for pool in stats["pools"]:
            pair_stats_dto.add_pool(
                name=pool["dexName"].lower(),
                stats=StatsDTO(
                    ada=pool["token2Amount"],
                    book=pool["token1Amount"],
                    daily_txs=pool["dailyTxAmount"],
                    daily_buys=pool["dailyBuysCount"],
                    daily_sales=pool["dailySalesCount"],
                    daily_volume=pool["dailyVolume"],
                    price_change_hour=pool["priceChangeHour"],
                    price_change_day=pool["priceChangeDay"],
                    price_change_week=pool["priceChangeWeek"],
                    price_change_month=pool["priceChangeMonth"],
                ),
            )

        return pair_stats_dto

    def last_orders(self, limit: int = 25) -> Iterable[OrderDTO]:
        orders = dexhunterio.get_global_orders(
            self.asset_id,
            partner_code=self.dexhunter_partner_code,
        )

        for index, order in enumerate(orders):
            if index == limit:
                break

            if order["token_id_in"] == dexhunterio.ADA:
                order_type = OrderType.BUY
                ada = order["amount_in"]
                book = order["actual_out_amount"]
            else:
                order_type = OrderType.SELL
                book = order["amount_in"]
                ada = order["actual_out_amount"]

            yield OrderDTO(
                address=order["user_address"],
                ada=ada,
                book=book,
                order_type=order_type,
                dex=order["dex"],
                tx_hash=order.get("update_tx_hash") or order["tx_hash"],
            )
