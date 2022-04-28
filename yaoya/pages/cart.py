import streamlit as st
from yaoya.models.cart import Cart
from yaoya.models.user import User
from yaoya.pages.base import BasePage
from yaoya.repositories.order import OrderMemoryRepository
from yaoya.sesseion import StreamlitSessionManager
from yaoya.usecases.order import order_commit


class CartPage(BasePage):
    def __init__(self, ssm: StreamlitSessionManager) -> None:
        self.title = "カート"
        self.page_id = "cart"
        self.ssm = ssm

    def render(self) -> None:
        cart: Cart = self.ssm.get("cart")
        current_user: User = self.ssm.get("user")
        order_repo: OrderMemoryRepository = self.ssm.get("order_repo")

        st.title(self.title)
        if current_user.role != "member":
            st.warning("会員専用ページです")
            return

        message_box = st.empty()

        # カートテーブルの表示
        col_size = [1, 2, 2, 2]
        columns = st.columns(col_size)
        headers = ["No", "商品名", "単価", "数量"]
        for col, field_name in zip(columns, headers):
            col.write(field_name)

        for cart_item in cart.items:
            (
                col1,
                col2,
                col3,
                col4,
            ) = st.columns(col_size)
            col1.write(cart_item.item_no)
            col2.write(cart_item.item_name)
            col3.write(cart_item.unit_price)
            col4.write(cart_item.quantity)

        # 注文処理
        def on_click() -> None:
            order_commit(cart, order_repo)

        if st.button("注文", on_click=on_click):
            message_box.info("注文が完了しました")
