from yaoya.models.cart import Cart
from yaoya.repositories.item import ItemMemoryStore
from yaoya.repositories.order import OrderDetailMemoryStore, OrderMemoryStore


def add_cart(item_store: ItemMemoryStore, cart: Cart, item_id: str, quantity: int, tax_ratio: float = 0.1) -> None:
    item = item_store.get_by_id(item_id)
    unit_price = item.price
    tax = int(unit_price * quantity * tax_ratio)
    subtotal_price = unit_price * quantity + tax
    cart.add_item(
        item_id=item.item_id,
        item_name=item.name,
        unit_price=unit_price,
        quantity=quantity,
        tax=tax,
        subtotal_price=subtotal_price,
    )


def order_commit(cart: Cart, order_store: OrderMemoryStore, order_detail_store: OrderDetailMemoryStore) -> None:
    if len(cart.items) == 0:
        return

    order_store.insert(
        order_id=cart.order_id,
        user_id=cart.user_id,
        total_price=cart.total_price,
    )
    for order_detail in cart.items:
        order_detail_store.insert(
            order_id=order_detail.order_id,
            order_no=order_detail.order_no,
            item_id=order_detail.item_id,
            unit_price=order_detail.unit_price,
            quantity=order_detail.quantity,
            tax=order_detail.tax,
            subtotal_price=order_detail.subtotal_price,
        )
    cart.clear()
