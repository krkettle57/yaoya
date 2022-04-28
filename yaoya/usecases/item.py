from yaoya.models.cart import Cart
from yaoya.repositories.item import ItemMemoryRepository


def add_cart(item_repo: ItemMemoryRepository, cart: Cart, item_id: str, quantity: int, tax_ratio: float = 0.1) -> None:
    item = item_repo.get_by_id(item_id)
    unit_price = item.price
    cart.add_item(
        item_id=item.item_id,
        item_name=item.name,
        unit_price=unit_price,
        quantity=quantity,
    )
