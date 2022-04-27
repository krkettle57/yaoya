from datetime import datetime, timedelta, timezone

import pandas as pd
from yaoya.repositories.base import MemoryStore


class OrderMemoryStore(MemoryStore):
    def __init__(self) -> None:
        self._df: pd.DataFrame = pd.DataFrame(columns=["order_id", "user_id", "total_price", "ordered_at"])
        self._tz = timezone(timedelta(hours=+9), "JST")

    def insert(self, order_id: str, user_id: str, total_price: int) -> None:
        row = dict(
            order_id=order_id,
            user_id=user_id,
            total_price=total_price,
            ordered_at=datetime.now(self._tz).strftime("%Y-%m-%d %H:%M:%S"),
        )
        super().insert(row)


class OrderDetailMemoryStore(MemoryStore):
    def __init__(self) -> None:
        self._df: pd.DataFrame = pd.DataFrame(
            columns=["order_id", "order_no", "item_id", "unit_price", "quantity", "tax", "subtotal_price"]
        )

    def insert(
        self, order_id: str, order_no: int, item_id: str, unit_price: int, quantity: int, tax: int, subtotal_price: int
    ) -> None:
        row = dict(
            order_id=order_id,
            order_no=order_no,
            item_id=item_id,
            unit_price=unit_price,
            quantity=quantity,
            tax=tax,
            subtotal_price=subtotal_price,
        )
        super().insert(row)
