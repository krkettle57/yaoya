import streamlit as st

from yaoya.pages.cart import cart_page
from yaoya.pages.item import item_page
from yaoya.pages.order import order_page
from yaoya.pages.user import user_page
from yaoya.repositories.item import ItemMemoryStore, item_mock_insert
from yaoya.repositories.order import OrderDetailMemoryStore, OrderMemoryStore
from yaoya.repositories.user import UserMemoryStore, user_mock_insert

# 初期化処理
if not st.session_state.get("started", False):
    # store初期化
    user_store = UserMemoryStore()
    user_mock_insert(user_store, n=1, role="admin")
    user_mock_insert(user_store, n=5, role="member")

    item_store = ItemMemoryStore()
    item_mock_insert(item_store, n=5, item_type="vegetable")
    item_mock_insert(item_store, n=5, item_type="fruit")

    # session初期化
    st.session_state["started"] = True
    st.session_state["user"] = None
    st.session_state["user_store"] = user_store
    st.session_state["item_store"] = item_store
    st.session_state["order_store"] = OrderMemoryStore()
    st.session_state["order_detail_store"] = OrderDetailMemoryStore()
    st.session_state["cart"] = None

    print("Complete initialized.")

PAGES = ["user", "item", "order", "cart"]


st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", PAGES)


def app() -> None:
    if selection == "user":
        user_page(st.session_state["user_store"])
        return

    elif selection == "item":
        user = st.session_state["user"]
        if user is None:
            st.warning("ログインが必要です")
            return

        item_page(st.session_state["cart"], st.session_state["item_store"])
        return

    elif selection == "order":
        user = st.session_state["user"]
        if user is None:
            st.warning("ログインが必要です")
            return

        if user.role != "admin":
            st.warning("権限が足りません")
            return

        order_page(
            st.session_state["order_store"],
            st.session_state["order_detail_store"],
        )
        return

    elif selection == "cart":
        user = st.session_state["user"]
        if user is None:
            st.warning("ログインが必要です")
            return

        cart_page(
            st.session_state["cart"],
            st.session_state["user"],
            st.session_state["order_store"],
            st.session_state["order_detail_store"],
        )
        return

    else:
        st.error("予期しないエラーが発生しました")
        return


app()
