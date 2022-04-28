from typing import List

from yaoya.models.order import Order


class OrderMemoryRepository:
    def __init__(self) -> None:
        self.orders: List[Order] = []

    def get_all(self) -> List[Order]:
        return self.orders

    def get_by_id(self, order_id: str) -> Order:
        orders = [order for order in self.orders if order.order_id == order_id]
        if len(orders) == 0:
            raise Exception()

        return orders[0]

    def insert(self, order: Order) -> None:
        self.orders.append(order)
