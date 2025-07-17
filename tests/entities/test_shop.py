from tegtory.domain.entities import Shop


def test_delivery_required() -> None:
    shop = Shop(id=1, title="", description="", distance=10)
    assert shop.delivery_required


def test_delivery_not_required() -> None:
    shop = Shop(id=1, title="", description="", distance=1)
    assert not shop.delivery_required
