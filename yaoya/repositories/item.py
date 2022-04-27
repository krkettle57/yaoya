from random import randint

from mimesis import Field, Schema
from mimesis.locales import Locale
from yaoya.models.item import Item, ItemType
from yaoya.repositories.base import MemoryStore


class ItemMemoryStore(MemoryStore):
    def get_by_id(self, item_id: str) -> Item:
        df = self._df
        item = df[df["item_id"] == item_id].to_dict("records")[0]
        return Item(
            item_id=item["item_id"],
            name=item["name"],
            price=item["price"],
            producing_area=item["producing_area"],
            item_type=item["item_type"],
        )

    def insert(self, item_id: str, name: str, price: str, producing_area: str, item_type: str) -> None:
        row = dict(
            item_id=item_id,
            name=name,
            price=price,
            producing_area=producing_area,
            item_type=item_type,
        )
        super().insert(row)


def item_mock_insert(item_store: ItemMemoryStore, n: int, item_type: ItemType) -> None:
    _ = Field(locale=Locale.JA)
    schema = Schema(
        schema=lambda: {
            "item_id": _("uuid"),
            "name": _(item_type),
            "price": randint(1, 5) * 100 - 2,
            "producing_area": _("prefecture"),
        }
    )
    for item in schema.create(n):
        item_store.insert(item["item_id"], item["name"], item["price"], item["producing_area"], item_type)
