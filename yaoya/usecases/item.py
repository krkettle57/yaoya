from yaoya.models.cart import Cart
from yaoya.models.order import Order
from yaoya.repositories.item import ItemMemoryRepository
from yaoya.repositories.order import OrderMemoryRepository


def add_cart(item_repo: ItemMemoryRepository, cart: Cart, item_id: str, quantity: int, tax_ratio: float = 0.1) -> None:
    item = item_repo.get_by_id(item_id)
    unit_price = item.price
    cart.add_item(
        item_id=item.item_id,
        item_name=item.name,
        unit_price=unit_price,
        quantity=quantity,
    )


def order_commit(cart: Cart, order_repo: OrderMemoryRepository) -> None:
    if len(cart.items) == 0:
        return

    order = Order(user_id=cart.user_id)
    for order_detail in cart.items:
        order.add_detail(
            order_detail.item_id,
            order_detail.unit_price,
            order_detail.quantity,
        )
    order_repo.insert(order)
    cart.clear()
