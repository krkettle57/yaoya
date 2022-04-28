from yaoya.models.cart import Cart
from yaoya.models.order import Order
from yaoya.repositories.order import OrderMemoryRepository


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
