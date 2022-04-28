from dataclasses import dataclass, field
from typing import List


@dataclass
class CartItem:
    item_no: int
    item_id: str
    item_name: str
    unit_price: int
    quantity: int


@dataclass
class Cart:
    user_id: str
    items: List[CartItem] = field(default_factory=list)

    def add_item(self, item_id: str, item_name: str, unit_price: int, quantity: int) -> None:
        item = CartItem(
            item_no=len(self.items) + 1,
            item_id=item_id,
            item_name=item_name,
            unit_price=unit_price,
            quantity=quantity,
        )
        self.items.append(item)

    def clear(self) -> None:
        self.items = []
