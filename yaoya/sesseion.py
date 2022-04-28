from dataclasses import dataclass
from enum import Enum, unique
from typing import Any, Optional

from streamlit import AutoSessionState

from yaoya.models.cart import Cart
from yaoya.models.user import User
from yaoya.repositories.item import ItemMemoryRepository
from yaoya.repositories.order import OrderMemoryRepository
from yaoya.repositories.user import UserMemoryRepository


@dataclass
class StreamlitSessionState:
    started: Optional[bool]
    user: Optional[User]
    cart: Optional[Cart]
    user_repo: Optional[UserMemoryRepository]
    item_repo: Optional[ItemMemoryRepository]
    order_repo: Optional[OrderMemoryRepository]


@unique
class StreamlitSessionKey(Enum):
    started = "started"
    user = "user"
    cart = "cart"
    user_repo = "user_repo"
    item_repo = "item_repo"
    order_repo = "order_repo"


class StreamlitSessionManager:
    def __init__(self, session_state: AutoSessionState) -> None:
        self.session_state = session_state

    def get(self, key: str) -> Any:
        return self.session_state[key]

    def set(self, sss: StreamlitSessionState) -> None:
        for key in sss.__annotations__.keys():
            value = getattr(sss, key)
            if value is not None:
                self.session_state[key] = value
