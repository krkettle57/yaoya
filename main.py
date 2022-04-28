import streamlit as st

from yaoya.models.cart import Cart
from yaoya.pages.base import MultiPageApp
from yaoya.pages.cart import CartPage
from yaoya.pages.item_list import ItemListPage
from yaoya.pages.login import LoginPage
from yaoya.pages.order_list import OrderListPage
from yaoya.repositories.item import ItemMemoryRepository, dummy_items_insert
from yaoya.repositories.order import OrderMemoryRepository
from yaoya.repositories.user import UserMemoryRepository, dummy_users_insert, get_dummy_users
from yaoya.sesseion import StreamlitSessionManager, StreamlitSessionState

# 初期化処理
if not st.session_state.get("started", False):
    # store初期化
    user_repo = UserMemoryRepository()
    guest_user = get_dummy_users(n=1, role="guest")[0]
    user_repo.insert(guest_user)
    dummy_users_insert(user_repo, n=1, role="admin")
    dummy_users_insert(user_repo, n=5, role="member")

    item_repo = ItemMemoryRepository()
    dummy_items_insert(item_repo, n=5, item_type="vegetable")
    dummy_items_insert(item_repo, n=5, item_type="fruit")

    # session初期化
    ssm = StreamlitSessionManager(st.session_state)
    sss = StreamlitSessionState(
        started=True,
        user=guest_user,
        cart=Cart(guest_user.user_id),
        user_repo=user_repo,
        item_repo=item_repo,
        order_repo=OrderMemoryRepository(),
    )
    ssm.set(sss)

    app = MultiPageApp(ssm)
    pages = [
        LoginPage(ssm),
        ItemListPage(ssm),
        CartPage(ssm),
        OrderListPage(ssm),
    ]
    for page in pages:
        app.add_page(page)
    st.session_state["app"] = app

app = st.session_state.get("app", None)
if app is not None:
    st.set_page_config(page_title="八百屋さんEC", layout="wide")
    app.render()
