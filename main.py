import streamlit as st

from yaoya.pages.cart import cart_page
from yaoya.pages.item import item_page
from yaoya.pages.order import order_page
from yaoya.pages.user import user_page
from yaoya.repositories.item import ItemMemoryRepository, dummy_items_insert
from yaoya.repositories.order import OrderMemoryRepository
from yaoya.repositories.user import UserMemoryRepository, dummy_users_insert

# 初期化処理
if not st.session_state.get("started", False):
    # store初期化
    user_repo = UserMemoryRepository()
    dummy_users_insert(user_repo, n=1, role="admin")
    dummy_users_insert(user_repo, n=5, role="member")

    item_repo = ItemMemoryRepository()
    dummy_items_insert(item_repo, n=5, item_type="vegetable")
    dummy_items_insert(item_repo, n=5, item_type="fruit")

    # session初期化
    st.session_state["started"] = True
    st.session_state["user"] = None
    st.session_state["user_repo"] = user_repo
    st.session_state["item_repo"] = item_repo
    st.session_state["order_repo"] = OrderMemoryRepository()
    st.session_state["cart"] = None

    print("Complete initialized.")

PAGES = ["user", "item", "cart", "order"]

st.set_page_config(page_title="八百屋さんEC", layout="wide", initial_sidebar_state="collapsed")
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", PAGES)


def app() -> None:
    if selection == "user":
        user_page(st.session_state["user_repo"])
        return

    elif selection == "item":
        user = st.session_state["user"]
        if user is None:
            st.warning("ログインが必要です")
            return

        item_page(st.session_state["cart"], st.session_state["item_repo"])
        return

    elif selection == "cart":
        user = st.session_state["user"]
        if user is None:
            st.warning("ログインが必要です")
            return

        cart_page(
            st.session_state["cart"],
            st.session_state["user"],
            st.session_state["order_repo"],
        )
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
            st.session_state["order_repo"],
        )
        return

    else:
        st.error("予期しないエラーが発生しました")
        return


app()
