from enum import EnumType

from tegtory.common.settings import ASSETS_DIR


class Images(EnumType):
    factory = ASSETS_DIR / "tegtory/factory.png"
    factory_hire = ASSETS_DIR / "tegtory/factory__hire.png"
    factory_tax = ASSETS_DIR / "tegtory/factory__tax.png"
    factory_upgrade = ASSETS_DIR / "tegtory/factory__upgrade.png"
    leaderboard = ASSETS_DIR / "tegtory/leaderboard.png"
    page = ASSETS_DIR / "tegtory/page.png"
    shop = ASSETS_DIR / "tegtory/shop.png"
    logistic_company = ASSETS_DIR / "tegtory/logistic_company.png"
    city = ASSETS_DIR / "tegtory/city.png"
