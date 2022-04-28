import pandas as pd
import streamlit as st
from yaoya.models.cart import Cart
from yaoya.models.user import User
from yaoya.repositories.order import OrderMemoryRepository
from yaoya.usecases.order import order_commit


def cart_page(cart: Cart, current_user: User, order_repo: OrderMemoryRepository) -> None:
    st.title("カート")
    message_box = st.empty()
    user_name = current_user.name

    # カートテーブルの表示
    show_cart_df = pd.DataFrame(
        [
            {
                "item_no": cart_item.item_no,
                "item_name": cart_item.item_name,
                "unit_price": cart_item.unit_price,
                "quantity": cart_item.quantity,
            }
            for cart_item in cart.items
        ]
    )
    st.subheader("カート")
    st.text(f"ユーザ名: {user_name}")
    st.dataframe(show_cart_df)

    # 注文処理
    def on_click() -> None:
        order_commit(cart, order_repo)

    if st.button("注文", on_click=on_click):
        message_box.info("注文が完了しました")
