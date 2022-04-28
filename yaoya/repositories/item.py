from random import randint
from typing import List

from mimesis import Field, Schema
from mimesis.locales import Locale
from yaoya.models.item import Item, ItemType
from yaoya.repositories.base import NotFoundError


class ItemMemoryRepository:
    def __init__(self) -> None:
        self.items: List[Item] = []

    def get_all(self) -> List[Item]:
        return self.items

    def get_by_id(self, item_id: str) -> Item:
        items = [item for item in self.items if item.item_id == item_id]
        if len(items) == 0:
            raise NotFoundError(item_id)

        return items[0]

    def insert(self, item: Item) -> None:
        self.items.append(item)


def get_dummy_items(n: int, item_type: ItemType) -> List[Item]:
    _ = Field(locale=Locale.JA)
    schema = Schema(
        schema=lambda: {
            "item_id": _("uuid"),
            "name": _(item_type),
            "price": randint(1, 5) * 100 - 2,
            "producing_area": _("prefecture"),
        }
    )
    items = [
        Item(
            item_id=data["item_id"],
            name=data["name"],
            price=data["price"],
            producing_area=data["producing_area"],
            item_type=item_type,
        )
        for data in schema.create(n)
    ]
    return items


def dummy_items_insert(item_repository: ItemMemoryRepository, n: int, item_type: ItemType) -> None:
    for item in get_dummy_items(n, item_type):
        item_repository.insert(item)
