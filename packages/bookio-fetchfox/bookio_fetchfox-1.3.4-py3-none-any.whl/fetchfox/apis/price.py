from fetchfox.apis import coingeckocom
from fetchfox.apis.cardano import muesliswap
from fetchfox.constants.book import BOOK_TOKEN_ASSET_ID
from fetchfox.constants.currencies import ADA, BOOK


def usd(currency: str) -> float:
    if currency == BOOK:
        ada = muesliswap.price(BOOK_TOKEN_ASSET_ID)

        return ada * coingeckocom.usd(ADA)
    else:
        return coingeckocom.usd(currency)
