from dataclasses import dataclass, field
from typing import List
from uuid import uuid4


@dataclass
class CartItem:
    order_id: str
    order_no: int
    item_id: str
    item_name: str
    unit_price: int
    quantity: int


@dataclass
class Cart:
    user_id: str
    order_id: str = field(init=False)
    order_no: int = field(init=False)
    total_price: int = field(init=False)
    items: List[CartItem] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self.clear()

    def add_item(self, item_id: str, item_name: str, unit_price: int, quantity: int) -> None:
        item = CartItem(
            order_id=self.order_id,
            order_no=self.order_no,
            item_id=item_id,
            item_name=item_name,
            unit_price=unit_price,
            quantity=quantity,
        )
        self.items.append(item)
        self.order_no += 1

    def clear(self) -> None:
        self.order_id = str(uuid4())
        self.order_no = 1
        self.total_price = 0
        self.items = []
